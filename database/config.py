""" Proxy module for database config.

Core classes for building declarative and automapped databases
"""

from pydantic import BaseSettings

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


