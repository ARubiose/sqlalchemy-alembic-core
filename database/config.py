# Core classes for building declarative and automapped databases
from database.core import *

# Import Base schema for declarative database
from database.models import Base

# TODO: Pydantic model for database config

# Example of declarative database
declarative_database = DeclarativeLiteDatabase(
    dialect='sqlite',
    driver='pysqlite',
    name='database.db',
    Base=Base
)

# Example of automapped database
automapped_database = AutoMappedLiteDatabase(
    dialect='sqlite',
    driver='pysqlite',
    name='database.db'
)
