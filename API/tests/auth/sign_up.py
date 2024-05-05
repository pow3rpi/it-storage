import random
from string import ascii_letters

from pydantic import ValidationError

from src.core.exceptions.user import (
    InvalidFirstname, InvalidPassword, PasswordsMismatch,
    EmailExists, InvalidUsername, UsernameExists, InvalidLastname
)
from src.schema.user import UserSignUpRequest
from tests.base import BaseTest


class SignUpTestCase(BaseTest):

    """
    We don't consider valid sign up test case because it can't be covered by module tests as
    sign up use case requires Redis and Email Service (external service) to be working
    """

    async def test_invalid_name(self):
        for name in self.invalid_names:
            with self.subTest(name):
                with self.assertRaises(InvalidFirstname):
                    await self.sign_up_use_case.sign_up(
                        UserSignUpRequest(
                            first_name=name, last_name=self.valid_lastname, username=self.valid_username,
                            email=self.valid_email, password=self.valid_password, password_confirm=self.valid_password_confirm
                        )
                    )
        for name in self.invalid_names:
            with self.subTest(name):
                with self.assertRaises(InvalidLastname):
                    await self.sign_up_use_case.sign_up(
                        UserSignUpRequest(
                            first_name=self.valid_firstname, last_name=name, username=self.valid_username,
                            email=self.valid_email, password=self.valid_password, password_confirm=self.valid_password_confirm
                        )
                    )

    async def test_invalid_password(self):
        for pwd in self.invalid_passwords:
            with self.subTest(pwd):
                with self.assertRaises(InvalidPassword):
                    await self.sign_up_use_case.sign_up(
                        UserSignUpRequest(
                            first_name=self.valid_firstname, last_name=self.valid_lastname,
                            username=self.valid_username, email=self.valid_email, password=pwd, password_confirm=pwd
                        )
                    )

    async def test_password_mismatch(self):
        with self.assertRaises(PasswordsMismatch):
            await self.sign_up_use_case.sign_up(
                UserSignUpRequest(
                    first_name=self.valid_firstname, last_name=self.valid_lastname, username=self.valid_username,
                    email=self.valid_email, password=self.valid_password, password_confirm=self.valid_password + random.choice(ascii_letters)
                )
            )

    async def test_invalid_email(self):
        for email in self.invalid_emails:
            with self.subTest(email):
                with self.assertRaises(ValidationError):
                    await self.sign_up_use_case.sign_up(
                        UserSignUpRequest(
                            first_name=self.valid_firstname, last_name=self.valid_lastname, username=self.valid_username,
                            email=email, password=self.valid_password, password_confirm=self.valid_password_confirm
                        )
                    )

    async def test_email_exists(self):
        user = await self.valid_sign_up()
        with self.assertRaises(EmailExists):
            await self.sign_up_use_case.sign_up(
                UserSignUpRequest(
                    first_name=self.valid_firstname_2, last_name=self.valid_lastname_2, email=user.email,
                    username=self.valid_username_2, password=self.valid_password_2, password_confirm=self.valid_password_confirm_2
                )
            )

    async def test_email_exists_2(self):
        user = await self.create_non_activated_user()
        with self.assertRaises(EmailExists):
            await self.sign_up_use_case.sign_up(
                UserSignUpRequest(
                    first_name=self.valid_firstname_2, last_name=self.valid_lastname_2, username=self.valid_username_2,
                    email=user.email, password=self.valid_password_2, password_confirm=self.valid_password_confirm_2
                )
            )

    async def test_invalid_username(self):
        for username in self.invalid_usernames:
            with self.subTest(username):
                with self.assertRaises(InvalidUsername):
                    await self.sign_up_use_case.sign_up(
                        UserSignUpRequest(
                            first_name=self.valid_firstname, last_name=self.valid_lastname, username=username,
                            email=self.valid_email, password=self.valid_password, password_confirm=self.valid_password_confirm
                        )
                    )

    async def test_username_exists(self):
        user = await self.valid_sign_up()
        with self.assertRaises(UsernameExists):
            await self.sign_up_use_case.sign_up(
                UserSignUpRequest(
                    first_name=self.valid_firstname_2, last_name=self.valid_lastname_2, username=user.username,
                    email=self.valid_email_2, password=self.valid_password_2, password_confirm=self.valid_password_confirm_2
                )
            )

    async def test_username_exists_2(self):
        user = await self.create_non_activated_user()
        with self.assertRaises(UsernameExists):
            await self.sign_up_use_case.sign_up(
                UserSignUpRequest(
                    first_name=self.valid_firstname_2, last_name=self.valid_lastname_2, username=user.username,
                    email=self.valid_email_2, password=self.valid_password_2, password_confirm=self.valid_password_confirm_2
                )
            )
