from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import EmailStr


@dataclass
class UserDto:
    id: int
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    hashed_pwd: str
    is_active: bool
    token: UUID = None


@dataclass
class TokenDto:
    username: str | None


@dataclass
class VerificationLinkDto:
    user_id: int
    email: str
    token: str
    creation_time: datetime


@dataclass
class VerificationDetailsDto:
    token: str
    creation_time: datetime
