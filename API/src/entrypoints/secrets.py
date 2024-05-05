from typing import Dict, Any

from pydantic import BaseSettings, AnyHttpUrl

env_file: str = '.env'


class AuthConfig(BaseSettings):
    ACCOUNT_ACTIVATION_URL: AnyHttpUrl
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES: int

    class Config:
        env_file: str = env_file


class SqlConfig(BaseSettings):
    SQL_USER: str
    SQL_PWD: str
    SQL_PORT: str
    SQL_HOST: str
    SQL_DATABASE: str
    SQL_URL: str

    def _build_values(self, *args, **kwargs) -> Dict[str, Any]:
        params = super(SqlConfig, self)._build_values(*args, **kwargs)
        params[
            'SQL_URL'
        ] = f"postgresql+asyncpg://{params['SQL_USER']}:{params['SQL_PWD']}@{params['SQL_HOST']}:{params['SQL_PORT']}/{params['SQL_DATABASE']}"
        return params

    class Config:
        env_file: str = env_file


class CeleryConfig(BaseSettings):
    CELERY_NAME: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file: str = env_file


class AppSecrets(BaseSettings):
    AUTH: AuthConfig = AuthConfig()
    SQL: SqlConfig = SqlConfig()
    CELERY: CeleryConfig = CeleryConfig()
