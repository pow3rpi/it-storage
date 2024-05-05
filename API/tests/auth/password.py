import random
from string import ascii_letters

from src.core.exceptions.user import (
    InvalidPassword, PasswordsMismatch, EqualPasswords, WrongPassword
)
from src.schema.user import ChangePasswordRequest
from tests.base import BaseTest


class ChangePasswordTestCase(BaseTest):

    """
    We don't consider valid sign up test case because it can't be covered by module tests as
    sign up use case requires Redis and Email Service (external service) to be working
    """

    async def test_invalid_current_password(self):
        user = await self.valid_sign_up()
        with self.assertRaises(WrongPassword):
            await self.change_password_use_case.change_password(
                user,
                ChangePasswordRequest(
                    current_password=self.valid_password + random.choice(ascii_letters),
                    password=self.valid_password_2, password_confirm=self.valid_password_confirm_2
                )
            )

    async def test_invalid_password(self):
        user = await self.valid_sign_up()
        for pwd in self.invalid_passwords:
            with self.subTest(pwd):
                with self.assertRaises(InvalidPassword):
                    await self.change_password_use_case.change_password(
                        user,
                        ChangePasswordRequest(
                            current_password=self.valid_password, password=pwd, password_confirm=pwd
                        )
                    )

    async def test_passwords_mismatch(self):
        user = await self.valid_sign_up()
        with self.assertRaises(PasswordsMismatch):
            await self.change_password_use_case.change_password(
                user,
                ChangePasswordRequest(
                    current_password=self.valid_password, password=self.valid_password_2,
                    password_confirm=self.valid_password_confirm_2 + random.choice(ascii_letters)
                )
            )

    async def test_equal_passwords(self):
        user = await self.valid_sign_up()
        with self.assertRaises(EqualPasswords):
            await self.change_password_use_case.change_password(
                user,
                ChangePasswordRequest(
                    current_password=self.valid_password, password=self.valid_password,
                    password_confirm=self.valid_password_confirm
                )
            )
