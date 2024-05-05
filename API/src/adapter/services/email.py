from celery import Celery

from src.core.enums import EmailTaskEnum
from src.interface.services.email import EmailServiceInterface


class EmailService(EmailServiceInterface):

    def __init__(self, celery_app: Celery):
        self.celery_app = celery_app

    async def send_sign_up_verification(self, email_to: str, verification_link: str):
        self.celery_app.send_task(EmailTaskEnum.InitSignUpNotifyTask.value, (email_to, verification_link,))

    async def send_notify_sign_up_verified(self, email_to: str):
        self.celery_app.send_task(EmailTaskEnum.SignUpNotifySuccessTask.value, (email_to,))

    async def send_notify_changed_password(self, email_to: str, username: str):
        self.celery_app.send_task(EmailTaskEnum.ChangePasswordNotifyTask.value, (email_to, username,))
