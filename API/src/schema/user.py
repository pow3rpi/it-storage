from __future__ import annotations
import string

from pydantic import BaseModel, EmailStr, validator, root_validator

from src.core import config
from src.core.exceptions.user import (
    InvalidUsername, InvalidFirstname, InvalidLastname,
    InvalidPassword, PasswordsMismatch
)


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None

    @validator('username')
    def validate_username(cls, v):
        v = v.strip().lower()
        if (
                len(v) < config.MIN_USERNAME_LENGTH
                or len(v) > config.MAX_USERNAME_LENGTH
                or not all(i.isdigit()
                           or i.isalpha()
                           or i in config.USERNAME_ALLOWED_CHARS for i in v)
                or v[0].isdigit()
                or v[0] in config.USERNAME_ALLOWED_CHARS
                or v[-1] in config.USERNAME_ALLOWED_CHARS
        ):
            raise InvalidUsername()
        return v

    @validator('email')
    def validate_email(cls, v):
        return v.lower()

    @validator('first_name')
    def validate_first_name(cls, v):
        if v:
            v = v.strip()
            if (
                    v
                    and (len(v) > config.MAX_NAME_LENGTH
                         or not v.isalpha())
            ):
                raise InvalidFirstname()
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if v:
            v = v.strip()
            if (
                    v
                    and (len(v) > config.MAX_NAME_LENGTH
                         or not v.isalpha())
            ):
                raise InvalidLastname()
        return v


class BasePassword(BaseModel):
    password: str
    password_confirm: str

    @validator('password')
    def validate_password(cls, v):
        if (
                len(v) < config.MIN_PWD_LENGTH
                or len(v) > config.MAX_PWD_LENGTH
                or not any(i.isdigit() for i in v)
                or not any(i.isalpha() for i in v)
                or not any(i in string.punctuation for i in v)
                or not any(i.isupper() for i in v)
                or not any(i.islower() for i in v)
                or ' ' in v

        ):
            raise InvalidPassword()
        return v

    @root_validator
    def validate_base_condition(cls, values):
        if values.get('password') != values.get('password_confirm'):
            raise PasswordsMismatch()
        return values


class UserSignUpRequest(BaseUser, BasePassword):
    pass


class UserLogInRequest(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        return v.lower()


class UserLogInResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserVerifyRequest(UserLogInResponse):
    refresh_token: str | None


class UserVerifyResponse(UserLogInResponse):
    pass


class UserUpdateRequest(BaseUser):
    pass


class ChangePasswordRequest(BasePassword):
    current_password: str
