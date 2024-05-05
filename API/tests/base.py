import unittest
from typing import List

import sqlalchemy as sa
from pydantic import EmailStr, AnyHttpUrl, StrictBytes

from src.adapter.celery_client import CeleryClient
from src.adapter.services.email import EmailService
from src.adapter.sql_db.base import Database
from src.adapter.sql_db.orm.blog import TagModel
from src.adapter.sql_db.orm.user import UserModel, SignUpVerificationModel
from src.adapter.sql_db.repository.link import LinkStorage
from src.adapter.sql_db.repository.post import PostStorage
from src.adapter.sql_db.repository.tutorial import TutorialStorage
from src.adapter.sql_db.repository.user import UserStorage
from src.core import config
from src.dto.blog import LinkDto, TutorialDto, TagDto
from src.dto.user import UserDto
from src.entrypoints.secrets import AppSecrets
from src.schema.link import CreateLinkRequest
from src.schema.tutorial import CreateTutorialRequest
from src.services.auth import AuthService
from src.usecase.auth.log_in import LogInUseCase
from src.usecase.auth.sign_up import SignUpUseCase
from src.usecase.auth.password import ChangePasswordUseCase
from src.usecase.auth.update import UpdateUserUseCase
from src.usecase.blog.link import LinkUseCase
from src.usecase.blog.post import PostUseCase
from src.usecase.blog.tutorial import TutorialUseCase


class BaseTest(unittest.IsolatedAsyncioTestCase):
    # user
    valid_user_id: int = 1
    valid_username: str = 'valid_user'
    valid_username_2: str = 'valid_user_2'
    valid_email: EmailStr = 'valid_user@example.com'
    valid_email_2: EmailStr = 'valid_user_2@example.com'
    valid_password: str = 'Valid_Pwd000'
    valid_password_2: str = 'Some123.PWD!_here'
    valid_password_confirm: str = valid_password
    valid_password_confirm_2: str = valid_password_2
    valid_firstname: str | None = 'Alex'
    valid_firstname_2: str | None = 'Steve'
    valid_lastname: str | None = None
    valid_lastname_2: str | None = 'Morgan'
    invalid_names: List[str] = [
        'A' * (config.MAX_NAME_LENGTH + 1),
        valid_firstname + '|'
    ]
    invalid_emails: List[str] = [
        'not an email',
        'example@',
        'example.com',
        'example@.com',
        'example@mail.',
        '@example.com',
        'exa mple@mail.com'
    ]
    invalid_usernames: List[str] = [
        'u' * (config.MIN_USERNAME_LENGTH - 1),
        'u' * (config.MAX_USERNAME_LENGTH + 1),
        'u' * config.MIN_USERNAME_LENGTH + '^',
        config.USERNAME_ALLOWED_CHARS[0] * config.MIN_USERNAME_LENGTH,
        config.USERNAME_ALLOWED_CHARS[0] + 'u' * config.MIN_USERNAME_LENGTH,
        'u' * config.MIN_USERNAME_LENGTH + config.USERNAME_ALLOWED_CHARS[0],
    ]
    invalid_passwords: List[str] = [
        'S.g5',
        'Aa1.' * (config.MAX_PWD_LENGTH // 4 + 1),
        '9302Kjda',
        '9302.-),',
        '___RftyT.',
        'lower45,.<>',
        '!1UPPER1!',
        '93=2Kj da'
    ]

    # post
    valid_post_id: int = 1
    valid_title: str = 'Valid title'
    valid_title_2: str = 'Valid title 2'
    valid_tags: List[str] | None = ['tag1', 'tag-2', 'valid-t']
    valid_tags_2: List[str] | None = ['tag1', 'tag-3']
    invalid_titles: List[str] = [
        't' * (config.MAX_TITLE_LENGTH + 1),
        't' * (config.MIN_TITLE_LENGTH - 1)
    ]
    invalid_tags: List[str] = [
        't' * (config.MAX_TAG_LENGTH + 1),
        't' * (config.MIN_TAG_LENGTH - 1),
        config.USERNAME_ALLOWED_CHARS[0] * config.MIN_TAG_LENGTH
    ]

    # link
    valid_url: AnyHttpUrl = 'https://valid.com'
    valid_url_2: AnyHttpUrl = 'https://valid_2.com'
    valid_annotation: str | None = 'Valid link annotation'
    valid_annotation_2: str | None = None
    invalid_urls: List[str] = [
        'not a http url',
        'http',
        'www.website.com',
        'http:website.com',
        'http//:website.com',
        'http:/website.com'
    ]
    invalid_annotation: str = 'a' * (config.MAX_ANNOTATION_LENGTH + 1)

    # tutorial
    valid_file: StrictBytes = 'Valid file text'
    valid_file_2: StrictBytes = 'Valid file text 2'

    async def asyncSetUp(self):
        secrets = AppSecrets()
        self.db = Database(url=secrets.SQL.SQL_URL)
        self.user_repo = UserStorage(session_factory=self.db.session)
        self.post_repo = PostStorage(session_factory=self.db.session)
        self.link_repo = LinkStorage(session_factory=self.db.session)
        self.tutorial_repo = TutorialStorage(session_factory=self.db.session)
        self.auth = AuthService(
            jwt_secret_key=secrets.AUTH.JWT_SECRET_KEY,
            access_token_expire_minutes=secrets.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES,
            jwt_refresh_secret_key=secrets.AUTH.JWT_REFRESH_SECRET_KEY,
            refresh_token_expire_minutes=secrets.AUTH.REFRESH_TOKEN_EXPIRE_MINUTES,
            algorithm=secrets.AUTH.ALGORITHM,
            repository=self.user_repo
        )
        self.celery_client = CeleryClient(
            name=secrets.CELERY.CELERY_NAME,
            broker_url=secrets.CELERY.CELERY_BROKER_URL,
            result_backend=secrets.CELERY.CELERY_RESULT_BACKEND,
        )
        self.email = EmailService(celery_app=self.celery_client.celery_app)
        self.log_in_use_case = LogInUseCase(self.user_repo, self.auth)
        self.sign_up_use_case = SignUpUseCase(
            self.user_repo, self.auth, self.email, secrets.AUTH.SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES
        )
        self.change_password_use_case = ChangePasswordUseCase(self.user_repo, self.auth, self.email)
        self.update_user_use_case = UpdateUserUseCase(
            self.user_repo, self.auth, secrets.AUTH.SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES
        )
        self.post_use_case = PostUseCase(self.post_repo)
        self.link_use_case = LinkUseCase(self.link_repo)
        self.tutorial_use_case = TutorialUseCase(self.tutorial_repo)

    async def asyncTearDown(self):
        async with self.db.session() as session:
            # pay attention that row SQL commands can vary from db to db
            await session.execute(sa.text(
                """
                    TRUNCATE TABLE 
                        "user", "base_post", "link_post", "tutorial_post",
                        "tag", "tag_post_association", "sign_up_verification" 
                    RESTART IDENTITY
                """
            ))
            await session.commit()

    async def valid_sign_up(self, second_user: bool = False, is_active: bool = True) -> UserDto:
        async with self.db.session() as session:
            """
            This thing is not implemented through corresponding use case because that use case can't be 
            completely covered by module tests as it requires Redis and Email Service (external service) to be working
            """
            if second_user:
                user = UserModel(
                    username=self.valid_username_2, first_name=self.valid_firstname_2, last_name=self.valid_lastname_2,
                    email=self.valid_email_2, password=self.auth.get_hashed_password(self.valid_password_2), is_active=is_active
                )
            else:
                user = UserModel(
                    username=self.valid_username, first_name=self.valid_firstname, last_name=self.valid_lastname,
                    email=self.valid_email, password=self.auth.get_hashed_password(self.valid_password), is_active=is_active
                )
            session.add(user)
            await session.commit()
            return UserDto(id=user.id, username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_pwd=user.password, is_active=user.is_active)

    async def create_non_activated_user(self) -> UserDto:
        user = await self.valid_sign_up(is_active=False)
        async with self.db.session() as session:
            token = SignUpVerificationModel(user_id=self.valid_user_id)
            session.add(token)
            await session.commit()
            return user

    async def create_valid_link(self, user: UserDto, second_post: bool = False) -> LinkDto:
        if second_post:
            return await self.link_use_case.create_link(
                user,
                CreateLinkRequest(
                    title=self.valid_title_2, url=self.valid_url, annotation=self.valid_annotation, tags=self.valid_tags_2
                )
            )
        return await self.link_use_case.create_link(
            user,
            CreateLinkRequest(
                title=self.valid_title, url=self.valid_url, annotation=self.valid_annotation, tags=self.valid_tags
            )
        )

    async def create_valid_tutorial(self, user: UserDto, second_post: bool = False) -> TutorialDto:
        if second_post:
            return await self.tutorial_use_case.create_tutorial(
                user,
                CreateTutorialRequest(title=self.valid_title_2, file=self.valid_file, tags=self.valid_tags_2)
            )
        return await self.tutorial_use_case.create_tutorial(
            user,
            CreateTutorialRequest(title=self.valid_title, file=self.valid_file, tags=self.valid_tags)
        )

    async def create_tags(self, tags: List[str]) -> List[TagDto]:
        async with self.db.session() as session:
            resp = []
            for tag in tags:
                new_tag = TagModel(name=tag)
                session.add(new_tag)
                resp.append(TagDto(id=new_tag.id, name=new_tag.name))
            await session.commit()
            return resp
