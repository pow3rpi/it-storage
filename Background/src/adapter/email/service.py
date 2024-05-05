import smtplib
from email.mime.multipart import MIMEMultipart

from src.adapter.email.factory import EmailMessageFactory
from src.interface.email import EmailServiceInterface


class EmailService(EmailServiceInterface):

    def __init__(self, email_host: str, email_port: int, email_from: str,
                 password: str, msg_factory: EmailMessageFactory = EmailMessageFactory()):
        self.email_host = email_host
        self.email_port = email_port
        self.email_from = email_from
        self.password = password
        self.msg_factory = msg_factory

    def _send_email(self, email_to: str, msg: str):
        with smtplib.SMTP_SSL(self.email_host, self.email_port) as smtp:
            smtp.login(self.email_from, self.password)
            smtp.sendmail(self.email_from, email_to, msg)

    def send_sign_up_verification(self, email_to: str, verification_link: str):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Account Activation'
        msg['From'] = self.email_from
        msg['To'] = email_to
        # build and send email message
        msg = self.msg_factory.build_sign_up_verification(msg, verification_link)
        self._send_email(email_to, msg)

    def send_sign_up_verification_successful(self, email_to: str):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Account Activation'
        msg['From'] = self.email_from
        msg['To'] = email_to
        # build and send email message
        msg = self.msg_factory.build_sign_up_verification_successful(msg)
        self._send_email(email_to, msg)

    def send_changed_pwd_notification(self, email_to: str, username: str):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'New Password'
        msg['From'] = self.email_from
        msg['To'] = email_to
        # build and send email message
        msg = self.msg_factory.build_changed_pwd_notification(msg, username)
        self._send_email(email_to, msg)
