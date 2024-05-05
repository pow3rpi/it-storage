from typing import Callable, List
from contextlib import AbstractAsyncContextManager

import sqlalchemy as sa
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapter.sql_db.orm.blog import LinkPostModel, BasePostModel
from src.adapter.sql_db.repository.post import PostStorage
from src.core.enums import PostEnum
from src.dto.blog import LinkDto
from src.interface.repository.link import LinkStorageInterface


class LinkStorage(LinkStorageInterface, PostStorage):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        super().__init__(session_factory)

    async def create_link(self, user_id: int, title: str, url: AnyHttpUrl,
                          annotation: str | None, tags: List[str] | None) -> LinkDto:
        async with self.session_factory() as session:
            link = LinkPostModel(url=url, annotation=annotation,
                                 title=title, author_id=user_id)
            if tags:
                # attach tags to the link post
                await self.create_tag(session, link, tags)
            session.add(link)
            await session.commit()
            return LinkDto(title=link.title, url=link.url, annotation=link.annotation,
                           tags=tags, post_id=link.post_id)

    async def get_link(self, user_id: int, post_id: int) -> LinkDto | None:
        async with self.session_factory() as session:
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == post_id,
                        BasePostModel.author_id == user_id,
                        BasePostModel.type == PostEnum.link.value) \
                .options(selectinload(BasePostModel.tag),
                         selectinload(BasePostModel.link_post))
            post = await session.execute(query)
            post = post.scalar()
            if post is None:
                return None
            tags = None
            if len(post.tag) > 0:
                tags = [tag.name for tag in post.tag]
            return LinkDto(post_id=post.id, title=post.title, tags=tags,
                           url=post.url, annotation=post.annotation)

    async def update_link(self, user_id: int, post_id: int, title: str, url: AnyHttpUrl,
                          annotation: str | None, tags: List[str] | None) -> LinkDto | None:
        async with self.session_factory() as session:
            # check if link post exists
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == post_id,
                        BasePostModel.author_id == user_id) \
                .options(selectinload(BasePostModel.tag))
            post = await session.execute(query)
            post = post.scalar()
            if not post:
                return None
            # update values
            post.title = title
            query = sa.update(LinkPostModel) \
                .returning(LinkPostModel.url, LinkPostModel.annotation) \
                .filter(LinkPostModel.post_id == post_id) \
                .values({'url': url, 'annotation': annotation})
            link = await session.execute(query)
            link = link.one()
            if tags:
                old_tags = sorted([tag.name for tag in post.tag])
                if old_tags != sorted(tags):
                    tags = await self.update_tags(session, post, tags)
            else:
                if len(post.tag) != 0:
                    tags = await self.update_tags(session, post, tags)
            session.add(post)
            await session.commit()
            return LinkDto(post_id=post.id, title=post.title, url=link.url,
                           annotation=link.annotation, tags=tags)
