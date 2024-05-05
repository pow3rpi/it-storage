from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:

    @staticmethod
    def _build_async_session(url: str) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(url, echo=False)
        session = async_sessionmaker(bind=engine, expire_on_commit=False)
        return session

    def __init__(self, url: str):
        self.session = self._build_async_session(url)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self.session()
        try:
            yield session
        except Exception:
            print("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
