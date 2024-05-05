from src.core.exceptions.user import InvalidCredentials, NonActivatedAccount
from src.dto.user import UserDto
from src.interface.repository.user import UserStorageInterface
from src.interface.services.auth import AuthServiceInterface
from src.schema.user import UserLogInResponse, UserLogInRequest


class LogInUseCase:

    def __init__(self,
                 repository: UserStorageInterface,
                 auth: AuthServiceInterface):
        self.repo = repository
        self.auth = auth

    async def _verify_username(self, username: str) -> UserDto:
        user = await self.repo.get_user(username=username)
        if not user:
            raise InvalidCredentials()
        return user

    def _verify_password(self, password: str, hashed_pwd_db: str):
        if not self.auth.verify_password(password, hashed_pwd_db):
            raise InvalidCredentials()

    async def _verify(self, data: UserLogInRequest):
        user = await self._verify_username(data.username)
        self._verify_password(data.password, user.hashed_pwd)
        activated = user.is_active
        if not activated:
            raise NonActivatedAccount()

    async def log_in(self, data: UserLogInRequest) -> UserLogInResponse:
        await self._verify(data)
        return UserLogInResponse(
            access_token=self.auth.create_access_token(data.username),
            refresh_token=self.auth.create_refresh_token(data.username)
        )
