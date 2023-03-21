import os
from abc import ABC


class Config(ABC):
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "statisticsuser")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "statisticsdb")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "statisticspass")
    SQL_COMMAND_ECHO = False


class DevelopmentConfig(Config):
    SQL_COMMAND_ECHO = True


def get_config() -> Config:
    env = os.getenv("ENV", "development") == "development"
    if env:
        return DevelopmentConfig()
    raise NotImplementedError


config = get_config()
