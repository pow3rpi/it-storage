import random
from string import ascii_letters

from src.core.exceptions.user import InvalidCredentials, NonActivatedAccount
from src.schema.user import UserLogInRequest, UserLogInResponse
from tests.base import BaseTest


class LogInTestCase(BaseTest):

    async def test_valid_log_in(self):
        user = await self.valid_sign_up()
        result = await self.log_in_use_case.log_in(
            UserLogInRequest(username=user.username, password=self.valid_password)
        )
        correct_result = UserLogInResponse(
            access_token=self.auth.create_access_token(user.username),
            refresh_token=self.auth.create_refresh_token(user.username)
        )
        self.assertEqual(result, correct_result)

    async def test_invalid_username(self):
        user = await self.valid_sign_up()
        with self.assertRaises(InvalidCredentials):
            await self.log_in_use_case.log_in(
                UserLogInRequest(
                    username=user.username + random.choice(ascii_letters), password=self.valid_password)
            )

    async def test_invalid_password(self):
        user = await self.valid_sign_up()
        with self.assertRaises(InvalidCredentials):
            await self.log_in_use_case.log_in(
                UserLogInRequest(
                    username=user.username, password=self.valid_password + random.choice(ascii_letters))
            )

    async def test_non_activated_account(self):
        user = await self.valid_sign_up(is_active=False)
        with self.assertRaises(NonActivatedAccount):
            await self.log_in_use_case.log_in(
                UserLogInRequest(username=user.username, password=self.valid_password))
