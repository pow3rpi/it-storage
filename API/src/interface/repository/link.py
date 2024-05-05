from abc import ABC, abstractmethod
from typing import List

from pydantic import AnyHttpUrl

from src.dto.blog import LinkDto


class LinkStorageInterface(ABC):

    @abstractmethod
    async def create_link(self,
                          user_id: int,
                          title: str,
                          url: AnyHttpUrl,
                          annotation: str | None,
                          tags: List[str] | None
                          ) -> LinkDto:
        raise NotImplemented()

    @abstractmethod
    async def get_link(self,
                       user_id: int,
                       post_id: int
                       ) -> LinkDto | None:
        raise NotImplemented()

    @abstractmethod
    async def update_link(self,
                          user_id: int,
                          post_id: int,
                          title: str,
                          url: AnyHttpUrl,
                          annotation: str | None,
                          tags: List[str] | None
                          ) -> LinkDto | None:
        raise NotImplemented()
