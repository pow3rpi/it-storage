from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):

    @abstractmethod
    def _send_email(self, email_to: str, msg: str):
        raise NotImplementedError()

    @abstractmethod
    def send_sign_up_verification(self, email_to: str, verification_link: str):
        raise NotImplementedError()

    @abstractmethod
    def send_sign_up_verification_successful(self, email_to: str):
        raise NotImplementedError()

    @abstractmethod
    def send_changed_pwd_notification(self, email_to: str, username: str):
        raise NotImplementedError()
