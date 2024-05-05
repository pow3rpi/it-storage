from src.core.exceptions.user import WrongPassword, EqualPasswords
from src.dto.user import UserDto
from src.interface.repository.user import UserStorageInterface
from src.interface.services.auth import AuthServiceInterface
from src.interface.services.email import EmailServiceInterface
from src.schema.user import ChangePasswordRequest


class ChangePasswordUseCase:

    def __init__(self,
                 repository: UserStorageInterface,
                 auth: AuthServiceInterface,
                 email: EmailServiceInterface):
        self.repo = repository
        self.auth = auth
        self.email = email

    def _validate(self, user: UserDto, data: ChangePasswordRequest):
        if not self.auth.verify_password(data.current_password, user.hashed_pwd):
            raise WrongPassword()
        if data.password == data.current_password:
            raise EqualPasswords()

    async def change_password(self, user: UserDto, data: ChangePasswordRequest) -> UserDto:
        self._validate(user, data)
        hashed_pwd = self.auth.get_hashed_password(data.password)
        user = await self.repo.change_password(
            user_id=user.id,
            new_hashed_pwd=hashed_pwd
        )
        # send email to notify that password has been changed
        await self.email.send_notify_changed_password(
            email_to=user.email,
            username=user.username
        )
        return user
