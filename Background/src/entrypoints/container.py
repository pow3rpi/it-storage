from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

from src.adapter.email.service import EmailService
from src.entrypoints.secrets import AppSecrets
from src.tasks.email import (
    ChangePasswordNotifyTask, SignUpNotifySuccessTask, InitSignUpNotifyTask
)

"""
This container describes and builds all dependencies in the application
"""


class AppContainer(DeclarativeContainer):
    config = Configuration(pydantic_settings=[AppSecrets()])

    email_service = Singleton(
        EmailService,
        email_host=config.EMAIL.EMAIL_HOST,
        email_port=config.EMAIL.EMAIL_PORT,
        email_from=config.EMAIL.EMAIL_FROM,
        password=config.EMAIL.EMAIL_PASSWORD
    )

    sign_up_notify_task = Singleton(
        InitSignUpNotifyTask,
        email_service=email_service
    )
    success_sign_up_notify_task = Singleton(
        SignUpNotifySuccessTask,
        email_service=email_service
    )
    change_pwd_notify_task = Singleton(
        ChangePasswordNotifyTask,
        email_service=email_service
    )
