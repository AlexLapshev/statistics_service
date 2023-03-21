from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class Database(ABC):
    def __init__(self):
        self.async_sessionmaker: Optional[sessionmaker] = None

    async def __call__(self) -> AsyncIterator[AsyncSession]:
        if not self.async_sessionmaker:
            raise ValueError("async_sessionmaker not available. Run setup() first.")
        async with self.async_sessionmaker() as session:
            yield session

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError


def get_connection_string(driver: str = "asyncpg") -> str:
    return f"postgresql+{driver}://{config.POSTGRES_USERNAME}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB_NAME}"


class PostgresDatabase(Database):
    def setup(self) -> None:
        async_engine = create_async_engine(
            get_connection_string(),
            echo=config.SQL_COMMAND_ECHO,
        )
        self.async_sessionmaker = sessionmaker(async_engine, class_=AsyncSession)