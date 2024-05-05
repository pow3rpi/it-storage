from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):

    @abstractmethod
    async def send_sign_up_verification(self,
                                        email_to: str,
                                        verification_link: str
                                        ) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def send_notify_sign_up_verified(self, email_to: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def send_notify_changed_password(self,
                                           email_to: str,
                                           username: str
                                           ) -> int:
        raise NotImplementedError()
