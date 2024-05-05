import logging.handlers

from src.core import config
from src.core.enums import APIHandlerEnum
from src.interface.logger import LoggerInterface


class Logger(LoggerInterface):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._file_handler = logging.handlers.RotatingFileHandler(
            filename=config.LOG_PATH + f'error_logs.log',
            mode='w',
            maxBytes=config.LOG_SIZE_IN_BYTES,
            backupCount=config.N_LOGS,
            encoding='utf-8'
        )
        self._formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)

    def log_error(self, handler: APIHandlerEnum, message: str):
        self._logger.error(f'{handler.value} - {message}')
