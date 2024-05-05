import sqlalchemy as sa

from pydantic import ValidationError

from src.adapter.sql_db.orm.user import UserModel
from src.core.exceptions.user import (
    InvalidFirstname, EmailExists, InvalidUsername,
    UsernameExists, InvalidLastname
)
from src.dto.user import UserDto
from src.schema.user import UserUpdateRequest
from tests.base import BaseTest


class UpdateUserTestCase(BaseTest):

    async def test_valid_update(self):
        user = await self.valid_sign_up()
        data = UserUpdateRequest(
            first_name=self.valid_firstname_2, last_name=self.valid_lastname_2,
            username=self.valid_username_2, email=self.valid_email_2
            )
        result = await self.update_user_use_case.update_user(user, data)
        correct_result = UserDto(
            id=user.id, username=data.username, email=data.email, first_name=data.first_name,
            last_name=data.last_name, hashed_pwd=user.hashed_pwd, is_active=user.is_active
        )
        self.assertEqual(result, correct_result)
        async with self.db.session() as session:
            # check that user has been updated
            query = sa.select(UserModel) \
                .filter(UserModel.id == user.id,
                        UserModel.first_name == data.first_name,
                        UserModel.last_name == data.last_name,
                        UserModel.username == data.username,
                        UserModel.email == data.email)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)

    async def test_invalid_name(self):
        user = await self.valid_sign_up()
        for name in self.invalid_names:
            with self.subTest(name):
                with self.assertRaises(InvalidFirstname):
                    await self.update_user_use_case.update_user(
                        user,
                        UserUpdateRequest(
                            first_name=name, last_name=user.last_name, username=user.username, email=user.email
                        )
                    )
        for name in self.invalid_names:
            with self.subTest(name):
                with self.assertRaises(InvalidLastname):
                    await self.update_user_use_case.update_user(
                        user,
                        UserUpdateRequest(
                            first_name=user.first_name, last_name=name, username=user.username, email=user.username
                        )
                    )

    async def test_invalid_email(self):
        user = await self.valid_sign_up()
        for email in self.invalid_emails:
            with self.subTest(email):
                with self.assertRaises(ValidationError):
                    await self.update_user_use_case.update_user(
                        user,
                        UserUpdateRequest(
                            first_name=user.first_name, last_name=user.last_name, username=user.username, email=email
                        )
                    )

    async def test_email_exists(self):
        user = await self.valid_sign_up()
        user_2 = await self.valid_sign_up(second_user=True)
        with self.assertRaises(EmailExists):
            await self.update_user_use_case.update_user(
                user,
                UserUpdateRequest(
                    first_name=user.first_name, last_name=user.last_name, username=user.username, email=user_2.email
                )
            )

    async def test_email_exists_2(self):
        user = await self.create_non_activated_user()
        user_2 = await self.valid_sign_up(second_user=True)
        with self.assertRaises(EmailExists):
            await self.update_user_use_case.update_user(
                user_2,
                UserUpdateRequest(
                    first_name=user_2.first_name, last_name=user_2.last_name, username=user_2.username, email=user.email
                )
            )

    async def test_invalid_username(self):
        user = await self.valid_sign_up()
        for username in self.invalid_usernames:
            with self.subTest(username):
                with self.assertRaises(InvalidUsername):
                    await self.update_user_use_case.update_user(
                        user,
                        UserUpdateRequest(
                            first_name=user.first_name, last_name=user.last_name, username=username, email=user.email
                        )
                    )

    async def test_username_exists(self):
        user = await self.valid_sign_up()
        user_2 = await self.valid_sign_up(second_user=True)
        with self.assertRaises(UsernameExists):
            await self.update_user_use_case.update_user(
                user,
                UserUpdateRequest(
                    first_name=user.first_name, last_name=user.last_name, username=user_2.username, email=user.email
                )
            )

    async def test_username_exists_2(self):
        user = await self.create_non_activated_user()
        user_2 = await self.valid_sign_up(second_user=True)
        with self.assertRaises(UsernameExists):
            await self.update_user_use_case.update_user(
                user_2,
                UserUpdateRequest(
                    first_name=user_2.first_name, last_name=user_2.last_name, username=user.username, email=user_2.email
                )
            )
