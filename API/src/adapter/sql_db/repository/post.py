from typing import Callable, List, Tuple
from contextlib import AbstractAsyncContextManager

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapter.sql_db.orm.blog import BasePostModel, TagModel
from src.core import config
from src.core.enums import SearchEnum
from src.dto.blog import TagDto, TutorialDto, LinkDto
from src.interface.repository.post import PostStorageInterface


class PostStorage(PostStorageInterface):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    @staticmethod
    async def create_tag(session: AsyncSession, post: BasePostModel, post_tags: List[str]) -> List[TagDto]:
        # create new tags
        query = sa.select(TagModel.name)
        tags_pool = await session.execute(query)
        tags_pool = set(tags_pool.scalars().all())
        new_tags = []
        for tag in post_tags:
            if tag not in tags_pool:
                new_tags.append(tag)
        tags_to_create = [TagModel(name=tag) for tag in new_tags]
        session.add_all(tags_to_create)
        # attach tags to post
        query = sa.select(TagModel) \
            .filter(TagModel.name.in_(post_tags))
        tags = await session.execute(query)
        tags = tags.scalars().all()
        for tag in tags:
            post.tag.append(tag)
        tags = [TagDto(id=tag.id, name=tag.name) for tag in tags]
        return tags

    async def get_tags(self, string: str) -> List[TagDto] | None:
        async with self.session_factory() as session:
            query = sa.select(TagModel) \
                .filter(TagModel.name.contains(string)) \
                .limit(config.MAX_SUGGESTED_TAGS)
            tags = await session.execute(query)
            tags = tags.scalars().all()
            tags = [TagDto(id=tag.id, name=tag.name) for tag in tags]
            return tags

    @staticmethod
    async def update_tags(session: AsyncSession, post: BasePostModel,
                          new_tags: List[str] | None) -> List[str] | None:
        if new_tags:
            # get all available tags
            query = sa.select(TagModel.id, TagModel.name)
            tags_pool = await session.execute(query)
            tags_pool = {name: tag_id for tag_id, name in tags_pool.all()}
            # get old tags
            old_tags = {tag.name: tag.id for tag in post.tag}
            # find tags to remove and remove them
            tags_to_remove = [tag_id for name, tag_id in old_tags.items() if name not in new_tags]
            post.tag = [tag for tag in post.tag if tag.id not in tags_to_remove]
            # find tags to attach and add them
            tags_to_attach = [tag for tag in new_tags if tag not in old_tags]
            if len(tags_to_attach) > 0:
                for tag in tags_to_attach:
                    if tag not in tags_pool:
                        new_tag = TagModel(name=tag)
                        session.add(new_tag)
                # attach tags to post
                query = sa.select(TagModel) \
                    .filter(TagModel.name.in_(tags_to_attach))
                tags = await session.execute(query)
                tags = tags.scalars().all()
                for tag in tags:
                    post.tag.append(tag)
            return new_tags
        # delete all associations of the post
        post.tag = []
        return None

    async def get_posts(self, user_id: int, search_type: SearchEnum,
                        offset: int) -> Tuple[List[LinkDto | TutorialDto], int]:
        async with self.session_factory() as session:
            # check which filter is set
            if search_type == SearchEnum.all:
                query = sa.select(BasePostModel.id) \
                    .filter(BasePostModel.author_id == user_id)
            else:
                query = sa.select(BasePostModel.id) \
                    .filter(BasePostModel.author_id == user_id,
                            BasePostModel.type == search_type.value)
            post_ids = await session.execute(query)
            post_ids = post_ids.scalars().all()
            # calculate total number of found posts
            n_posts = len(post_ids)
            if not post_ids:
                return [], n_posts
            # get posts according to offset and limit
            start_index = config.MAX_POSTS_PER_PAGE * offset
            end_index = start_index + config.MAX_POSTS_PER_PAGE
            post_ids = post_ids[start_index:end_index]
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id.in_(post_ids)) \
                .options(selectinload(BasePostModel.tag),
                         selectinload(BasePostModel.link_post))
            posts = await session.execute(query)
            posts = list(posts.scalars().all())
            # generate data transfer objects (dto)
            for i in range(len(posts)):
                if posts[i].type == SearchEnum.link.value:
                    posts[i] = LinkDto(post_id=posts[i].id, title=posts[i].title,
                                       tags=[tag.name for tag in posts[i].tag],
                                       url=posts[i].url, annotation=posts[i].annotation)
                else:
                    posts[i] = TutorialDto(post_id=posts[i].id, title=posts[i].title,
                                           tags=[tag.name for tag in posts[i].tag], file='')
            return posts, n_posts

    async def get_posts_by_tags(self, user_id: int, tags: List[str], search_type: SearchEnum,
                                offset: int) -> Tuple[List[LinkDto | TutorialDto], int]:
        async with self.session_factory() as session:
            # find post ids which satisfy search conditions
            query = sa.text(f"""
                SELECT tag_post_association.id
                FROM (
                    SELECT tag_post_association.post_id AS id, 
                           ARRAY_LENGTH(ARRAY_AGG(tag_post_association.tag_id), 1) AS n_intersections
                    FROM tag_post_association
                    WHERE tag_post_association.post_id IN (
                        SELECT base_post.id
                        FROM base_post
                        WHERE base_post.author_id = :user_id {'AND base_post.type = :post_type' if search_type != SearchEnum.all else ''}
                    )
                      AND tag_post_association.tag_id IN (
                        SELECT tag.id
                        FROM tag
                        WHERE tag.name IN :tags
                    )
                    GROUP BY tag_post_association.post_id
                    ORDER BY n_intersections DESC
                ) AS tag_post_association
            """)
            query = query.bindparams(
                sa.bindparam('tags', expanding=True)
            )  # it is needed to put arrays into row sql
            post_ids = await session.execute(
                query,
                {'user_id': user_id, 'post_type': search_type.value, 'tags': tags}
            )
            post_ids = post_ids.scalars().all()
            # calculate total number of found posts
            n_posts = len(post_ids)
            if not post_ids:
                return [], n_posts
            # get posts according to offset and limit
            start_index = config.MAX_POSTS_PER_PAGE * offset
            end_index = start_index + config.MAX_POSTS_PER_PAGE
            post_ids = post_ids[start_index:end_index]
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id.in_(post_ids)) \
                .options(selectinload(BasePostModel.tag),
                         selectinload(BasePostModel.link_post))  # if you add new params to tutorial, attach it here
            posts = await session.execute(query)
            posts = list(posts.scalars().all())
            # generate data transfer objects (dto)
            for i in range(len(posts)):
                if posts[i].type == SearchEnum.link.value:
                    posts[i] = LinkDto(post_id=posts[i].id, title=posts[i].title,
                                       tags=[tag.name for tag in posts[i].tag],
                                       url=posts[i].url, annotation=posts[i].annotation)
                else:
                    posts[i] = TutorialDto(post_id=posts[i].id, title=posts[i].title,
                                           tags=[tag.name for tag in posts[i].tag], file='')
            # sort the result
            posts.sort(key=lambda post: post_ids.index(post.post_id))
            return posts, n_posts

    async def get_posts_by_title(self, user_id: int, string: str, search_type: SearchEnum,
                                 offset: int) -> Tuple[List[LinkDto | TutorialDto], int]:
        async with self.session_factory() as session:
            query = sa.text(f"""
                SELECT id
                FROM (
                    SELECT id, similarity_score
                    FROM (
                        SELECT id, similarity(base_post.title, :string) AS similarity_score
                        FROM base_post
                        WHERE author_id = :user_id {'AND type = :post_type' if search_type != SearchEnum.all else ''}
                    ) AS base_post
                    WHERE similarity_score > :min_score
                    ORDER BY similarity_score DESC
                ) AS base_post
            """)
            post_ids = await session.execute(
                query,
                {'string': string, 'user_id': user_id, 'post_type': search_type.value,
                 'min_score': config.MIN_SIMILARITY_SCORE}
            )
            post_ids = post_ids.scalars().all()
            # calculate total number of found posts
            n_posts = len(post_ids)
            if not post_ids:
                return [], n_posts
            # get posts according to offset and limit
            start_index = config.MAX_POSTS_PER_PAGE * offset
            end_index = start_index + config.MAX_POSTS_PER_PAGE
            post_ids = post_ids[start_index:end_index]
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id.in_(post_ids)) \
                .options(selectinload(BasePostModel.tag),
                         selectinload(BasePostModel.link_post))  # if you add new params to tutorial, attach it here
            posts = await session.execute(query)
            posts = list(posts.scalars().all())
            # generate data transfer objects (dto)
            for i in range(len(posts)):
                if posts[i].type == SearchEnum.link.value:
                    posts[i] = LinkDto(post_id=posts[i].id, title=posts[i].title,
                                       tags=[tag.name for tag in posts[i].tag],
                                       url=posts[i].url, annotation=posts[i].annotation)
                else:
                    posts[i] = TutorialDto(post_id=posts[i].id, title=posts[i].title,
                                           tags=[tag.name for tag in posts[i].tag], file='')
            # sort the result
            posts.sort(key=lambda post: post_ids.index(post.post_id))
            return posts, n_posts

    async def delete_post(self, user_id: int, post_id: List[int]):
        async with self.session_factory() as session:
            query = sa.delete(BasePostModel) \
                .filter(BasePostModel.id.in_(post_id),
                        BasePostModel.author_id == user_id)
            await session.execute(query)
            await session.commit()
