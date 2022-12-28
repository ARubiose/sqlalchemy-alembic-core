""" Proxy module for database config.

Core classes for building declarative and automapped databases
"""
from pydantic import BaseSettings
from database import Database

# Import Base schema for declarative database
from database.models import Base

class DatabaseSettings(BaseSettings):
    """Database settings for database connection"""
    DIALECT:    str
    DRIVER:     str
    NAME:       str
    USER:       str = None
    PASSWORD:   str = None

    class Config:
        """Config for pydantic settings model"""
        env_file = '.env'

settings = DatabaseSettings()

database = Database(
    dialect=settings.DIALECT,
    driver=settings.DRIVER,
    name=settings.NAME,
    Base=Base,
    user=settings.USER,
    password=settings.PASSWORD
)

# Example of declarative database
# declarative_database = LiteDatabase(
#     dialect='sqlite',
#     driver='pysqlite',
#     name='database.db',
#     Base=Base
# )

# Example of automapped database with user and password
# database = AutoMappedDatabase(
#     dialect='mysql',
#     driver='pymysql',
#     name='database',
#     user='root',
#     password='',
# )
