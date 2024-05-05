import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.adapter.sql_db.base import Base
from src.adapter.sql_db.orm.user import *
from src.adapter.sql_db.orm.blog import *
from src.entrypoints.secrets import AppSecrets

SQL_URL = AppSecrets().SQL.SQL_URL
config = context.config
config.set_main_option('sqlalchemy.url', SQL_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    async_engine = create_async_engine(SQL_URL)

    def do_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    async with async_engine.connect() as connection:
        await connection.run_sync(do_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
