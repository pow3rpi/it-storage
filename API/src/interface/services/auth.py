from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.dto.user import UserDto, TokenDto
from src.schema.user import UserVerifyRequest, UserVerifyResponse


class AuthServiceInterface(ABC):

    @abstractmethod
    def get_hashed_password(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def verify_password(self,
                        password: str,
                        hashed_pwd: str
                        ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def create_access_token(self,
                            subject: Any,
                            expires_delta: int = None
                            ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def create_refresh_token(self,
                             subject: Any,
                             expires_delta: int = None
                             ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def extract_token_data(self,
                           token: str,
                           secret_key: str
                           ) -> TokenDto:
        raise NotImplementedError()

    @abstractmethod
    async def verify_user(self, tokens: UserVerifyRequest) -> UserVerifyResponse | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_current_user(self, token: str) -> UserDto:
        raise NotImplementedError()

    @abstractmethod
    def generate_verification_link(self, token: UUID, username: str) -> str:
        raise NotImplementedError()
