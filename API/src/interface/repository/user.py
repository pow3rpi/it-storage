from abc import ABC, abstractmethod

from pydantic import EmailStr

from src.dto.user import UserDto, VerificationLinkDto, VerificationDetailsDto


class UserStorageInterface(ABC):

    @abstractmethod
    async def create_user(self,
                          username: str,
                          email: EmailStr,
                          first_name: str | None,
                          last_name: str | None,
                          hashed_pwd: str
                          ) -> UserDto:
        raise NotImplemented()

    @abstractmethod
    async def get_user(self, **attributes) -> UserDto | None:
        raise NotImplemented()

    @abstractmethod
    async def verify_sign_up_token(self,
                                   token: str,
                                   username: str
                                   ) -> VerificationLinkDto | None:
        raise NotImplemented()

    @abstractmethod
    async def get_verification_details(self, user_id: int) -> VerificationDetailsDto:
        raise NotImplemented()

    @abstractmethod
    async def activate_user(self, user_id: int, email: str):
        raise NotImplemented()

    @abstractmethod
    async def update_user(self,
                          user_id: int,
                          username: str,
                          email: EmailStr,
                          first_name: str | None,
                          last_name: str | None,
                          ) -> UserDto:
        raise NotImplemented()

    @abstractmethod
    async def change_password(self,
                              user_id: int,
                              new_hashed_pwd: str
                              ) -> UserDto:
        raise NotImplemented()

    @abstractmethod
    async def delete_user(self, **attributes):
        raise NotImplemented()
