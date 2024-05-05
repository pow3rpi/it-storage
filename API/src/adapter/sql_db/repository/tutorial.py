from typing import Callable, List
from contextlib import AbstractAsyncContextManager

import sqlalchemy as sa
from pydantic import StrBytes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapter.sql_db.orm.blog import TutorialPostModel, BasePostModel
from src.adapter.sql_db.repository.post import PostStorage
from src.core.enums import PostEnum
from src.dto.blog import TutorialDto
from src.interface.repository.tutorial import TutorialStorageInterface


class TutorialStorage(TutorialStorageInterface, PostStorage):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        super().__init__(session_factory)

    async def create_tutorial(self, user_id: int, title: str, file: StrBytes,
                              tags: List[str] | None) -> TutorialDto:
        async with self.session_factory() as session:
            tutorial = TutorialPostModel(file=file, title=title, author_id=user_id)
            if tags:
                # attach tags to the tutorial post
                await self.create_tag(session, tutorial, tags)
            session.add(tutorial)
            await session.commit()
            return TutorialDto(title=tutorial.title, file=tutorial.file,
                               tags=tags, post_id=tutorial.post_id)

    async def get_tutorial(self, user_id: int, post_id: int) -> TutorialDto | None:
        async with self.session_factory() as session:
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == post_id,
                        BasePostModel.author_id == user_id,
                        BasePostModel.type == PostEnum.tutorial.value) \
                .options(selectinload(BasePostModel.tag),
                         selectinload(BasePostModel.tutorial_post))
            post = await session.execute(query)
            post = post.scalar()
            if post is None:
                return None
            tags = None
            if len(post.tag) > 0:
                tags = [tag.name for tag in post.tag]
            return TutorialDto(post_id=post.id, title=post.title,
                               tags=tags, file=post.file)

    async def update_tutorial(self, user_id: int, post_id: int, title: str, file: StrBytes,
                              tags: List[str] | None) -> TutorialDto | None:
        async with self.session_factory() as session:
            # check if tutorial post exists
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
            query = sa.update(TutorialPostModel) \
                .returning(TutorialPostModel.file) \
                .filter(TutorialPostModel.post_id == post_id) \
                .values({'file': file})
            file = await session.execute(query)
            file = file.scalar()
            if tags:
                old_tags = sorted([tag.name for tag in post.tag])
                if old_tags != sorted(tags):
                    tags = await self.update_tags(session, post, tags)
            else:
                if len(post.tag) != 0:
                    tags = await self.update_tags(session, post, tags)
            session.add(post)
            await session.commit()
            return TutorialDto(post_id=post.id, title=post.title,
                               tags=tags, file=file)
