from contextlib import AbstractAsyncContextManager
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapter.sql_db.orm.user import UserModel, SignUpVerificationModel
from src.dto.user import UserDto, VerificationLinkDto, VerificationDetailsDto
from src.interface.repository.user import UserStorageInterface


class UserStorage(UserStorageInterface):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def create_user(self, username: str, first_name: str | None, last_name: str | None,
                          email: str, hashed_pwd: str) -> UserDto:
        async with self.session_factory() as session:
            user = UserModel(username=username, first_name=first_name,
                             last_name=last_name, email=email, password=hashed_pwd)
            # generate verification token
            verification = SignUpVerificationModel(user=user)
            session.add_all([user, verification])
            await session.commit()
            return UserDto(id=user.id, username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_pwd=user.password, is_active=user.is_active,
                           token=verification.token)

    async def get_user(self, **attributes) -> UserDto | None:
        async with self.session_factory() as session:
            query = sa.select(UserModel) \
                .filter_by(**attributes)
            user = await session.execute(query)
            user = user.scalar()
            if user is None:
                return None
            return UserDto(id=user.id, username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_pwd=user.password, is_active=user.is_active)

    async def activate_user(self, user_id: int, email: str):
        async with self.session_factory() as session:
            query = sa.update(UserModel) \
                .filter(UserModel.email == email) \
                .values({'is_active': True})
            await session.execute(query)
            query = sa.update(SignUpVerificationModel) \
                .filter(SignUpVerificationModel.user_id == user_id) \
                .values({'is_used': True})
            await session.execute(query)
            await session.commit()

    async def verify_sign_up_token(self, token: str, username: str) -> VerificationLinkDto | None:
        async with self.session_factory() as session:
            query = sa.select(SignUpVerificationModel) \
                .filter(SignUpVerificationModel.user.has(username == username),
                        SignUpVerificationModel.token == token,
                        SignUpVerificationModel.is_used.is_(False)) \
                .options(selectinload(SignUpVerificationModel.user))
            verify_token = await session.execute(query)
            verify_token = verify_token.scalar()
            if not verify_token:
                return None
            return VerificationLinkDto(user_id=verify_token.user_id, email=verify_token.user.email,
                                       creation_time=verify_token.creation_time, token=verify_token.token)

    async def get_verification_details(self, user_id: int) -> VerificationDetailsDto:
        async with self.session_factory() as session:
            query = sa.select(SignUpVerificationModel) \
                .filter(SignUpVerificationModel.user_id == user_id)
            details = await session.execute(query)
            details = details.scalar()
            return VerificationDetailsDto(token=details.token, creation_time=details.creation_time)

    async def update_user(self, user_id: int, username: str, first_name: str | None,
                          last_name: str | None, email: str) -> UserDto:
        async with self.session_factory() as session:
            query = sa.update(UserModel) \
                .returning(UserModel) \
                .filter(UserModel.id == user_id) \
                .values({'username': username, 'first_name': first_name,
                         'last_name': last_name, 'email': email})
            user = await session.execute(query)
            user = user.scalar()
            await session.commit()
            return UserDto(id=user.id, username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_pwd=user.password, is_active=user.is_active)

    async def change_password(self, user_id: int, new_hashed_pwd: str) -> UserDto:
        async with self.session_factory() as session:
            query = sa.update(UserModel) \
                .returning(UserModel) \
                .filter(UserModel.id == user_id) \
                .values({'password': new_hashed_pwd})
            user = await session.execute(query)
            user = user.scalar()
            await session.commit()
            return UserDto(id=user.id, username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_pwd=user.password, is_active=user.is_active)

    async def delete_user(self, **attributes):
        async with self.session_factory() as session:
            query = sa.delete(UserModel) \
                .filter_by(**attributes)
            await session.execute(query)
            await session.commit()
