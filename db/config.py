# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# DATABASE_URL = "postgresql+asyncpg://statisticsuser:statisticspass@localhost:5432/statisticsdb"
# engine = create_async_engine(DATABASE_URL, future=False, echo=True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
# Base = declarative_base()
import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    SQL_COMMAND_ECHO = False


class DevelopmentConfig(Config):
    SQL_COMMAND_ECHO = True


def get_config() -> Config:
    env = os.getenv("ENV") == "development"
    if env == "development":
        return DevelopmentConfig()
    raise NotImplementedError


config = get_config()
