# Core classes for building declarative and automapped databases
from database.core import Database, AutoMappedDatabase #, LiteDatabase, AutoMappedDatabase, AutoMappedLiteDatabase

# Import Base schema for declarative database
from database.models import Base

# TODO: Pydantic model for database config

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

database = Database(
    dialect='mysql',
    driver='pymysql',
    name='database',
    Base=Base,
    user='root',
    password='',
)
