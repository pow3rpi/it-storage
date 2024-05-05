from abc import ABC, abstractmethod
from typing import List

from pydantic import StrBytes

from src.dto.blog import TutorialDto


class TutorialStorageInterface(ABC):

    @abstractmethod
    async def create_tutorial(self,
                              user_id: int,
                              title: str,
                              file: StrBytes,
                              tags: List[str] | None
                              ) -> TutorialDto:
        raise NotImplemented()

    @abstractmethod
    async def get_tutorial(self,
                           user_id: int,
                           post_id: int
                           ) -> TutorialDto | None:
        raise NotImplemented()

    @abstractmethod
    async def update_tutorial(self,
                              user_id: int,
                              post_id: int,
                              title: str,
                              file: StrBytes,
                              tags: List[str] | None
                              ) -> TutorialDto | None:
        raise NotImplemented()
