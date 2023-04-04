""" Database factory module """
from database.database import DeclarativeDatabase, AutoMappedDatabase, DeclarativeLiteDatabase, AutoMappedLiteDatabase

# Import Base schema for declarative database
from database.models.base import Base

# Import models for declarative base population
from database.models import *

# Import settings for database connection
from database.config import settings, BASE_DIR

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