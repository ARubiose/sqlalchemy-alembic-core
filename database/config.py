""" Proxy module for database config.

Core classes for building declarative and automapped databases
"""

from pydantic import BaseSettings
from database import DeclarativeDatabase, AutoMappedDatabase, DeclarativeLiteDatabase

# Import Base schema for declarative database
from database.models import Base

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

# Example of declarative database
database = DeclarativeDatabase(
    dialect=settings.DIALECT,
    driver=settings.DRIVER,
    name=settings.NAME,
    Base=Base,
    user=settings.USER,
    password=settings.PASSWORD
)

# Example of declarative lite database
lite_database = DeclarativeLiteDatabase(
    dialect='sqlite',
    driver='pysqlite',
    name='database.db',
    Base=Base,
    create_tables=True,
)

# Example of automapped database with user and password
# database = AutoMappedDatabase(
#     dialect='mysql',
#     driver='pymysql',
#     name='database',
#     user='root',
#     password='',
# )
