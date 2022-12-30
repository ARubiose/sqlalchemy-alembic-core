import pytest

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from database.database import LiteDatabaseConnection, AuthDatabaseConnection, DeclarativeLiteDatabase, AutoMappedLiteDatabase

@pytest.fixture
def lite_dialect():
    return "sqlite"

@pytest.fixture
def lite_driver():
    return "pysqlite"

@pytest.fixture
def mysql_dialect():
    return "mysql"

@pytest.fixture
def mysql_driver():
    return "pymysql"

@pytest.fixture
def database_name():
    return "database"

@pytest.fixture
def user_name():
    return "user"

@pytest.fixture
def user_password():
    return "***"

@pytest.fixture
def user_host():
    return "localhost"

@pytest.fixture
def user_port():
    return 5432

@pytest.fixture
def lite_database_connection( lite_dialect, lite_driver, database_name ):
    return LiteDatabaseConnection(
        dialect = lite_dialect,
        driver  = lite_driver,
        name    = database_name
    )

@pytest.fixture
def auth_database_connection( mysql_dialect, mysql_driver, database_name, user_name, user_password, user_host, user_port ):
    
    # It requires the database driver to be installed
    return AuthDatabaseConnection(
        dialect = mysql_dialect,
        driver  = mysql_driver,
        name    = database_name,
        user    = user_name,
        password= user_password,
        host    = user_host,
        port    = user_port
    )

@pytest.fixture
def declarative_lite_database( lite_dialect, lite_driver, database_name, base, tmp_path):
    return DeclarativeLiteDatabase(
        dialect = lite_dialect,
        driver  = lite_driver,
        name    = tmp_path / database_name,
        Base= base,
        create_tables = True
    )

@pytest.fixture
def base():
    Base = declarative_base()

    class Item(Base):
        __tablename__ = "items"
        id      = Column(Integer, primary_key=True)
        name    = Column(String(50), nullable=True)

    return Base

# Tests
def test_lite_database_connection(lite_database_connection: LiteDatabaseConnection):
    """Test that connection to a SQLite database match SQLAlchemy engine connection."""    

    sqlalchemy_url = lite_database_connection.engine.url

    assert sqlalchemy_url.render_as_string() == lite_database_connection.connection_string
    assert sqlalchemy_url.get_driver_name() == lite_database_connection.engine.driver
    assert sqlalchemy_url.get_dialect().name == lite_database_connection.engine.dialect.name
    assert sqlalchemy_url.database == lite_database_connection.name

def test_database_connection(auth_database_connection: AuthDatabaseConnection):
    """Test that connection to a SQL database match SQLAlchemy engine connection."""    

    sqlalchemy_url = auth_database_connection.engine.url

    assert sqlalchemy_url.render_as_string() == auth_database_connection.connection_string
    assert sqlalchemy_url.get_driver_name() == auth_database_connection.engine.driver
    assert sqlalchemy_url.get_dialect().name == auth_database_connection.engine.dialect.name
    assert sqlalchemy_url.database == auth_database_connection.name
    assert sqlalchemy_url.username == auth_database_connection.user
    assert sqlalchemy_url.password == auth_database_connection.password
    assert sqlalchemy_url.host == auth_database_connection.host
    assert sqlalchemy_url.port == auth_database_connection.port

def test_declarative_table_names(declarative_lite_database: DeclarativeLiteDatabase):
    """Test that the declarative base is working properly."""
    assert "items" in declarative_lite_database.get_table_names()