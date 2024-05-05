from datetime import datetime, timedelta

from pydantic import EmailStr

from src.core.exceptions.user import InvalidVerificationLink, UsernameExists, EmailExists
from src.dto.user import UserDto, VerificationLinkDto
from src.interface.repository.user import UserStorageInterface
from src.interface.services.auth import AuthServiceInterface
from src.interface.services.email import EmailServiceInterface
from src.schema.user import UserSignUpRequest


class SignUpUseCase:

    def __init__(self,
                 repository: UserStorageInterface,
                 auth: AuthServiceInterface,
                 email: EmailServiceInterface,
                 link_expire: int):
        self.repo = repository
        self.auth = auth
        self.email = email
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

    async def _validate(self, data: UserSignUpRequest):
        # check if username exists
        await self._validate_username(data.username)
        # check if email exists
        await self._validate_email(data.email)

    async def sign_up(self, data: UserSignUpRequest) -> UserDto:
        await self._validate(data)
        user = await self.repo.create_user(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_pwd=self.auth.get_hashed_password(data.password)
        )
        link = self.auth.generate_verification_link(user.token, user.username)
        # send email with verification link
        await self.email.send_sign_up_verification(
            email_to=user.email,
            verification_link=link
        )
        return user

    async def _verify(self, token: str, username: str) -> VerificationLinkDto:
        verify_token = await self.repo.verify_sign_up_token(token, username)
        if not verify_token:
            raise InvalidVerificationLink()
        # check if token is expired
        if datetime.now() - verify_token.creation_time > timedelta(minutes=self.link_expire):
            raise InvalidVerificationLink()
        return verify_token

    async def verify_sign_up(self, token: str, username: str) -> bool:
        try:
            verify_token = await self._verify(token, username)
            await self.repo.activate_user(verify_token.user_id, verify_token.email)
            # send email to notify that registration has been finished successfully
            await self.email.send_notify_sign_up_verified(verify_token.email)
            return True
        except InvalidVerificationLink:
            return False
