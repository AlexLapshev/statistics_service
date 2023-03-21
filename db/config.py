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
    if env:
        return DevelopmentConfig()
    raise NotImplementedError


config = get_config()
