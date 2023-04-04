""" Database factory module """
from database import DeclarativeDatabase, AutoMappedLiteDatabase, DeclarativeLiteDatabase

# Import Base schema for declarative database
from database.models import Base

# Import settings for database connection
from database.config import settings

# Example of declarative database
lite_database = DeclarativeDatabase(
    dialect=settings.DIALECT,
    driver=settings.DRIVER,
    name=settings.NAME,
    Base=Base,
    user=settings.USER,
    password=settings.PASSWORD
)
""" Example of declarative database using envornment variables."""

# Example of declarative lite database
lite_database = DeclarativeLiteDatabase(
    dialect='sqlite',
    driver='pysqlite',
    name='database.db',
    Base=Base,
    create_tables=True,
)
"""Example of declarative lite database."""

# Example of automapped database with user and password
automapped_database = AutoMappedLiteDatabase(
    dialect='sqlite',
    driver='pysqlite',
    name='database.db'
)
"""Example of automapped lite database."""