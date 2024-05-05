from abc import ABC, abstractmethod

from src.core.enums import APIHandlerEnum


class LoggerInterface(ABC):

    @abstractmethod
    def log_error(self, handler: APIHandlerEnum, message: str):
        raise NotImplementedError()
