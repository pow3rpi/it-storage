from datetime import datetime, timedelta

from pydantic import EmailStr

from src.core.exceptions.user import UsernameExists, EmailExists
from src.dto.user import UserDto
from src.interface.repository.user import UserStorageInterface
from src.interface.services.auth import AuthServiceInterface
from src.schema.user import UserUpdateRequest


class UpdateUserUseCase:

    def __init__(self,
                 repository: UserStorageInterface,
                 auth: AuthServiceInterface,
                 link_expire: int):
        self.repo = repository
        self.auth = auth
        self.link_expire = link_expire

    async def _validate_username(self, username: str):
        user = await self.repo.get_user(username=username)
        if user:
            if user.is_active:
                raise UsernameExists()
            # check if there is non-activated account but which still has time to be activated
            verification_details = await self.repo.get_verification_details(user_id=user.id)
            if datetime.now() - verification_details.creation_time < timedelta(minutes=self.link_expire):
                raise UsernameExists()
            await self.repo.delete_user(id=user.id)

    async def _validate_email(self, email: EmailStr):
        user = await self.repo.get_user(email=email)
        if user:
            if user.is_active:
                raise EmailExists()
            # check if there is non-activated account but which still has time to be activated
            verification_details = await self.repo.get_verification_details(user_id=user.id)
            if datetime.now() - verification_details.creation_time < timedelta(minutes=self.link_expire):
                raise EmailExists()
            await self.repo.delete_user(id=user.id)

    async def _validate(self, user: UserDto, data: UserUpdateRequest):
        if data.username != user.username:
            # check if username exists
            await self._validate_username(data.username)
        if data.email != user.email:
            # check if email exists
            await self._validate_email(data.email)

    async def update_user(self, user: UserDto, data: UserUpdateRequest) -> UserDto:
        await self._validate(user, data)
        user = await self.repo.update_user(
            user_id=user.id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email
        )
        return user
