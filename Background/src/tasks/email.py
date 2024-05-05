from celery import Task

from src.interface.email import EmailServiceInterface


class InitSignUpNotifyTask(Task):
    name = 'InitSignUpNotifyTask'

    def __init__(self, email_service: EmailServiceInterface):
        self._email_service = email_service

    def run(self, email_to: str, link: str, *args, **kwargs):
        self._email_service.send_sign_up_verification(email_to, link)


class SignUpNotifySuccessTask(Task):
    name = 'SignUpNotifySuccessTask'

    def __init__(self, email_service: EmailServiceInterface):
        self._email_service = email_service

    def run(self, email_to: str, *args, **kwargs):
        self._email_service.send_sign_up_verification_successful(email_to)


class ChangePasswordNotifyTask(Task):
    name = 'ChangePasswordNotifyTask'

    def __init__(self, email_service: EmailServiceInterface):
        self._email_service = email_service

    def run(self, email_to: str, username: str, *args, **kwargs):
        self._email_service.send_changed_pwd_notification(email_to, username)
