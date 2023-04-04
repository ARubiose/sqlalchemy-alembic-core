""" Database factory module """
import logging

from sqltoolbox.database import DeclarativeDatabase, AutoMappedDatabase, DeclarativeLiteDatabase, AutoMappedLiteDatabase

# Import Base schema for declarative database
from sqltoolbox.models.base import Base

# Import models for declarative base population
from sqltoolbox.models import *

# Import settings for database connection
from sqltoolbox.config import settings

logger = logging.getLogger('database')

# Example of declarative database
def get_declarative_database():
    """Factory function to get declarative database."""
    return DeclarativeDatabase(
        dialect=settings.DIALECT,
        driver=settings.DRIVER,
        name=settings.NAME,
        Base=Base,
        user=settings.USER,
        password=settings.PASSWORD
    )

def get_declarative_lite_database():
    """Factory function to get declarative lite database."""
    return DeclarativeLiteDatabase(
        dialect='sqlite',
        driver='pysqlite',
        name= 'data/database.db',
        Base=Base,
        create_tables=True,
    )

def get_automapped_lite_database():
    """Factory function to get automapped lite database."""
    return AutoMappedLiteDatabase(
        dialect='sqlite',
        driver='pysqlite',
        name= 'data/database.db',
    )