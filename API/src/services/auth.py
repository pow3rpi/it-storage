from datetime import datetime, timedelta
from typing import Any
from uuid import UUID
import urllib.parse

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import AnyHttpUrl

from src.core.exceptions.user import InvalidToken
from src.dto.user import UserDto, TokenDto
from src.schema.user import UserVerifyRequest, UserVerifyResponse
from src.interface.repository.user import UserStorageInterface
from src.interface.services.auth import AuthServiceInterface


class AuthService(AuthServiceInterface):

    def __init__(self,
                 account_activation_url: AnyHttpUrl,
                 jwt_secret_key: str,
                 access_token_expire_minutes: int,
                 jwt_refresh_secret_key: str,
                 refresh_token_expire_minutes: int,
                 algorithm: str,
                 repository: UserStorageInterface):
        self.account_activation_url = account_activation_url
        self.pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.jwt_secret_key = jwt_secret_key
        self.jwt_refresh_secret_key = jwt_refresh_secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        self.repo = repository

    def get_hashed_password(self, password: str) -> str:
        return self.pwd_ctx.hash(password)

    def verify_password(self, password: str, hashed_pwd: str) -> bool:
        return self.pwd_ctx.verify(password, hashed_pwd)

    def create_access_token(self, subject: Any, expires_delta: int = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        expire = datetime.utcnow() + expires_delta

        to_encode = {'exp': expire, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret_key, self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, subject: Any, expires_delta: int = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=self.refresh_token_expire_minutes)
        expire = datetime.utcnow() + expires_delta

        to_encode = {'exp': expire, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.jwt_refresh_secret_key, self.algorithm)
        return encoded_jwt

    def extract_token_data(self, token: str, secret_key: str) -> TokenDto:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            username: str = payload.get('sub')
            if username is None:
                raise InvalidToken()
            token_data = TokenDto(username=username)
        except JWTError or ExpiredSignatureError:
            raise InvalidToken()
        return token_data

    async def verify_user(self, tokens: UserVerifyRequest) -> UserVerifyResponse | None:
        try:
            token_data = self.extract_token_data(tokens.access_token, self.jwt_secret_key)
            new_tokens = None
        except InvalidToken:
            token_data = self.extract_token_data(tokens.refresh_token, self.jwt_refresh_secret_key)
            new_tokens = UserVerifyResponse(
                access_token=self.create_access_token(token_data.username),
                refresh_token=self.create_refresh_token(token_data.username)
            )
        user = await self.repo.get_user(username=token_data.username)
        if user is None or not user.is_active:
            raise InvalidToken()
        return new_tokens

    async def get_current_user(self, token: str) -> UserDto:
        token_data = self.extract_token_data(token, self.jwt_secret_key)
        user = await self.repo.get_user(username=token_data.username)
        if user is None or not user.is_active:
            raise InvalidToken()
        return user

    def generate_verification_link(self, token: UUID, username: str) -> str:
        url = f'{self.account_activation_url}?'
        params = {
            'token': token,
            'username': username
        }
        url = url + urllib.parse.urlencode(params)
        return url
