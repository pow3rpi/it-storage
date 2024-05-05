from dependency_injector import containers, providers

from src.adapter.celery_client import CeleryClient
from src.adapter.services.email import EmailService
from src.adapter.sql_db.base import Database
from src.adapter.sql_db.repository.link import LinkStorage
from src.adapter.sql_db.repository.post import PostStorage
from src.adapter.sql_db.repository.tutorial import TutorialStorage
from src.adapter.sql_db.repository.user import UserStorage
from src.core.logger import Logger
from src.entrypoints.secrets import AppSecrets
from src.services.auth import AuthService
from src.usecase.auth.log_in import LogInUseCase
from src.usecase.auth.password import ChangePasswordUseCase
from src.usecase.auth.sign_up import SignUpUseCase
from src.usecase.auth.update import UpdateUserUseCase
from src.usecase.blog.link import LinkUseCase
from src.usecase.blog.post import PostUseCase
from src.usecase.blog.tutorial import TutorialUseCase

"""
This container describes and builds all dependencies in the application
"""


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[AppSecrets()])

    # database
    db = providers.Singleton(Database, url=config.SQL.SQL_URL)
    user_repo = providers.Singleton(UserStorage, session_factory=db.provided.session)
    post_repo = providers.Singleton(PostStorage, session_factory=db.provided.session)
    link_repo = providers.Singleton(LinkStorage, session_factory=db.provided.session)
    tutorial_repo = providers.Singleton(TutorialStorage, session_factory=db.provided.session)

    # services
    auth_service = providers.Factory(
        AuthService,
        account_activation_url=config.AUTH.ACCOUNT_ACTIVATION_URL,
        jwt_secret_key=config.AUTH.JWT_SECRET_KEY,
        access_token_expire_minutes=config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES,
        jwt_refresh_secret_key=config.AUTH.JWT_REFRESH_SECRET_KEY,
        refresh_token_expire_minutes=config.AUTH.REFRESH_TOKEN_EXPIRE_MINUTES,
        algorithm=config.AUTH.ALGORITHM,
        repository=user_repo
    )
    celery_client = providers.Singleton(
        CeleryClient,
        name=config.CELERY.CELERY_NAME,
        broker_url=config.CELERY.CELERY_BROKER_URL,
        result_backend=config.CELERY.CELERY_RESULT_BACKEND,
    )
    email_service = providers.Factory(
        EmailService,
        celery_app=celery_client.provided.celery_app
    )

    # utils
    logger = providers.Singleton(Logger)

    # use cases
    sign_up_use_case = providers.Factory(
        SignUpUseCase,
        repository=user_repo,
        auth=auth_service,
        email=email_service,
        link_expire=config.AUTH.SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES
    )
    log_in_use_case = providers.Factory(
        LogInUseCase,
        repository=user_repo,
        auth=auth_service
    )
    change_password_use_case = providers.Factory(
        ChangePasswordUseCase,
        repository=user_repo,
        auth=auth_service,
        email=email_service
    )
    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        repository=user_repo,
        auth=auth_service,
        link_expire=config.AUTH.SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES
    )
    link_use_case = providers.Factory(
        LinkUseCase,
        repository=link_repo
    )
    tutorial_use_case = providers.Factory(
        TutorialUseCase,
        repository=tutorial_repo
    )
    post_use_case = providers.Factory(
        PostUseCase,
        repository=post_repo
    )
