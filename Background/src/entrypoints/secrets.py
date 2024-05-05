from pydantic import BaseSettings

env_file: str = '.env'


class CeleryConfig(BaseSettings):
    CELERY_NAME: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file: str = env_file


class EmailConfig(BaseSettings):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_FROM: str
    EMAIL_PASSWORD: str

    class Config:
        env_file: str = env_file


class AppSecrets(BaseSettings):
    CELERY: CeleryConfig = CeleryConfig()
    EMAIL: EmailConfig = EmailConfig()
