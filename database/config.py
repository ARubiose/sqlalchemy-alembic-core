""" Proxy module for database config.

Core classes for building declarative and automapped databases
"""
from pathlib import Path
from pydantic import BaseSettings

BASE_DIR = Path(__file__).parents[2].resolve()

class LiteDatabaseSettings(BaseSettings):
    """Database settings for database connection"""
    DIALECT:    str
    DRIVER:     str
    NAME:       str

    class Config:
        """Config for pydantic settings model"""
        env_file = '.env'

class DatabaseSettings(LiteDatabaseSettings):
    """Database settings for database connection"""
    USER:       str
    PASSWORD:   str

settings = DatabaseSettings()


