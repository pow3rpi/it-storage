from abc import ABC, abstractmethod
from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapter.sql_db.orm.blog import BasePostModel
from src.core.enums import SearchEnum
from src.dto.blog import TagDto, LinkDto, TutorialDto


class PostStorageInterface(ABC):

    @staticmethod
    @abstractmethod
    async def create_tag(session: AsyncSession,
                         post: BasePostModel,
                         post_tags: List[str]
                         ) -> List[TagDto]:
        raise NotImplemented()

    @abstractmethod
    async def get_tags(self, string: str) -> List[TagDto] | None:
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    async def update_tags(session: AsyncSession,
                          post: BasePostModel,
                          new_tags: List[str] | None
                          ) -> List[str] | None:
        raise NotImplemented()

    @abstractmethod
    async def get_posts(self,
                        user_id: int,
                        search_type: SearchEnum,
                        offset: int
                        ) -> Tuple[List[LinkDto | TutorialDto], int]:
        raise NotImplemented()

    @abstractmethod
    async def get_posts_by_tags(self,
                                user_id: int,
                                tags: List[str],
                                search_type: SearchEnum,
                                offset: int
                                ) -> Tuple[List[LinkDto | TutorialDto], int]:
        raise NotImplemented()

    @abstractmethod
    async def get_posts_by_title(self,
                                 user_id: int,
                                 string: str,
                                 search_type: SearchEnum,
                                 offset: int
                                 ) -> Tuple[List[LinkDto | TutorialDto], int]:
        raise NotImplemented()

    @abstractmethod
    async def delete_post(self, user_id: int, post_id: List[int]):
        raise NotImplemented()
