import pytest
import typing
from pathlib import Path

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from database.database import DeclarativeLiteDatabase, AutoMappedLiteDatabase, DeclarativeDatabase, AutoMappedDatabase

DB_DIR = Path(__file__).parent / "database"

@pytest.fixture
def base():
    Base = declarative_base()

    class Item(Base):
        __tablename__ = "items"
        id      = Column(Integer, primary_key=True)
        name    = Column(String(50), nullable=True)

    return Base

@pytest.fixture
def declarative_lite_db_connection( base : typing.Any ):
    """Generate a lite database connection with declarative Base."""
    return DeclarativeLiteDatabase(
        dialect = "sqlite",
        driver  = "pysqlite",
        name    = DB_DIR / "test_db.db",
        Base    = base,
    )

@pytest.fixture
def declarative_db_connection( base: typing.Any):
    """Generate a database connection with declarative Base. Requires database server to be running."""
    return DeclarativeDatabase(
        dialect = "mysql",
        driver  = "pymysql",
        name    = "test",
        user    = "root",
        password= "",
        Base    = base,
    )

@pytest.fixture
def automapped_lite_db_connection( ):
    """Generate a lite database with automapped Base."""
    return AutoMappedLiteDatabase(
        dialect = "sqlite",
        driver  = "pysqlite",
        name    = DB_DIR / "test_db.db",
    )

@pytest.fixture
def automapped_db_connection( ):
    """Generate a database connection with automapped Base. Requires database server to be running."""
    return AutoMappedDatabase(
        dialect = "mysql",
        driver  = "pymysql",
        name    = "test",
        user    = "root",
        password= "",
    )

# Tests
def test_lite_database_connection_attrs(declarative_lite_db_connection: DeclarativeLiteDatabase):
    """Test that connection to a SQLite database match SQLAlchemy engine connection."""    

    sqlalchemy_url = declarative_lite_db_connection.engine.url

    assert sqlalchemy_url.render_as_string() == declarative_lite_db_connection.connection_string
    assert sqlalchemy_url.get_driver_name() == declarative_lite_db_connection.engine.driver
    assert sqlalchemy_url.get_dialect().name == declarative_lite_db_connection.engine.dialect.name
    assert sqlalchemy_url.database == str(declarative_lite_db_connection.name)

def test_database_connection_attrs(declarative_db_connection: DeclarativeDatabase):
    """Test that connection to a SQL database match SQLAlchemy engine connection."""    

    sqlalchemy_url = declarative_db_connection.engine.url

    assert sqlalchemy_url.get_driver_name() == declarative_db_connection.engine.driver
    assert sqlalchemy_url.get_dialect().name == declarative_db_connection.engine.dialect.name
    assert sqlalchemy_url.database == declarative_db_connection.name
    assert sqlalchemy_url.username == declarative_db_connection.user
    assert sqlalchemy_url.password == declarative_db_connection.password
    assert sqlalchemy_url.host == declarative_db_connection.host
    assert sqlalchemy_url.port == declarative_db_connection.port

def test_table_names(declarative_lite_db_connection: DeclarativeLiteDatabase):
    """Test that the declarative base is working properly."""
    assert "items" in declarative_lite_db_connection.get_table_names()

def test_automapped_table_names(automapped_lite_db_connection: AutoMappedLiteDatabase):
    """Test that the automapped base is working properly."""
    assert "items" in automapped_lite_db_connection.get_table_names()

def test_engine_type(declarative_lite_db_connection: DeclarativeLiteDatabase):
    """Test that the engine is a SQLAlchemy engine."""
    assert isinstance(declarative_lite_db_connection.engine, sqlalchemy.engine.Engine)