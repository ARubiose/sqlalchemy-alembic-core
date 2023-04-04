""" Core module containing classes for Engine+Base combinations"""
import abc
import typing
import logging
from typing import Protocol
from dataclasses import dataclass, field

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base

from sqltoolbox.models.base import create_declarative_base

__all__ = [
    'DeclarativeDatabase',
    'DeclarativeLiteDatabase',
    'AutoMappedDatabase',
    'AutoMappedLiteDatabase',
    'create_declarative_base',
]

logger = logging.getLogger('database')

@dataclass(kw_only=True)
class DatabaseConnection(abc.ABC):
    """Base abstract class representing minimal database connection data for SQLALchemy.
    
    It creates a SQLAlchemy engine and a session factory.
    
    Attributes:
        dialect (str): The dialect of the database.
        driver (str): The driver used to access the database.
        name (str): The name of the database.
        echo (bool, optional): Controls the verbosity of the engine. Defaults to False.
        future (bool, optional): Use the SQLAlchemy 2.0 API. Defaults to True.
        engine_args (Dict[str, Any], optional): Additional arguments to be passed to the engine creation. Defaults to an empty dictionary.
        session (Session): A session object. It generates a new session for each call. Use it with a context manager.
        autocommit_session (Session): A session object that begins a transaction. Use it with a context manager.
        engine (Engine): An engine object.

    Raises:
        NotImplementedError: Raised if the method _create_connection_string is not implemented.
"""
    dialect:    str
    driver:     str
    name:       str
    # Additional connection arguments
    echo:           bool = False
    future:         bool = True
    engine_args:    typing.Dict[str, typing.Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._engine: sqlalchemy.engine.Engine = self.generate_engine()
        self._session_factory = sessionmaker(self._engine)
        super().__post_init__()

    @property
    def session(self) -> Session:
        """Property for a session object that generates a new session for each call. 
        
        Only read access is allowed and it must be used with a context manager.
        
        Returns:
            Session: A session object
        """
        return self._session_factory()

    @property
    def autocommit_session(self) -> Session:
        """Property for a session that automatically commits the transaction when the context manager exits. 
        
        Only read access is allowed and it must be used with a context manager.
        
        Returns:
            Session: A session object
        """
        return self._session_factory.begin()

    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        """Property for the engine associated to the object
        
        Returns:
            Engine: A SQLAlchemy engine object
        """
        return self._engine

    @engine.setter
    def engine(self, engine: sqlalchemy.engine.Engine) -> None:
        """Setter for the engine property. It checks if the engine is a valid SQLAlchemy engine.
        
        Args:
            engine (Engine): A SQLAlchemy engine object
            
        Raises:
            TypeError: Raised if the engine is not a valid SQLAlchemy engine.
        """
        if not isinstance(engine, sqlalchemy.engine.Engine):
            raise TypeError(f"Expected sqlalchemy.engine.Engine, got {type(engine)}")
        self._engine = engine

    @property
    def connection_string(self) -> str:
        """ Property for the connection string associated to the object.

        Only read access is allowed.
        
        Returns:
            str: A connection string
        """
        return self._create_connection_string()

    # Engine factory methods
    def generate_engine(self, name: typing.Optional[str] = None) -> sqlalchemy.engine.Engine:
        """Method for creating a new engine object for the given database name.
        
        Args:
            name (Optional[str], optional): The name of the database. Defaults to None. If None, the name of the object is used.

        Returns:
            Engine: A SQLAlchemy engine object  
        """
        connection_string: str = self._create_connection_string(name=name if name else self.name)
        return sqlalchemy.create_engine(connection_string, echo=self.echo, future=self.future, **self.engine_args)

    def get_engines_from_list(self, database_list: typing.List[str]) -> typing.Dict[str, sqlalchemy.engine.Engine]:
        """Method for creating a dictionary with multiple engines for the given database names.
        
        Args:
            database_list (List[str]): A list of database names.

        Returns:
            Dict[str, Engine]: A dictionary with the database names as keys and the SQLAlchemy engine objects as values.
        """
        return {name: self.generate_engine(name=name) for name in database_list}

    @abc.abstractmethod
    def _create_connection_string(self, name:typing.Optional[str] = None) -> str:
        """ Method for creating connection string for database 
        
        Args:
            name (Optional[str], optional): The name of the database. Defaults to None. If None, the name of the object is used.
            
        Raises:
            NotImplementedError: Raised if the method is not implemented.
        """
        raise NotImplementedError

@dataclass(kw_only=True)
class LiteDatabaseConnection(DatabaseConnection, abc.ABC):
    """ Lite connection abstract class representing minimal database connection data for SQLALchemy. """

    def _create_connection_string(self, name:typing.Optional[str] = None) -> str:
        """ Method for creating connection string for sqlite database"""
        if name:
            return f"{self.dialect}+{self.driver}:///{name}"
        return f"{self.dialect}+{self.driver}:///{self.name}"


@dataclass(kw_only=True)
class AuthDatabaseConnection(DatabaseConnection, abc.ABC):
    """ Complete connection abstract class representing complete database connection data for SQLALchemy.
    
    Attributes:
        user (str): The user name to authenticate with.
        password (str): The password to authenticate with.
        port (Optional[int], optional): The port to connect to. Defaults to None. SQLAlchemy will use the default port for the given dialect.
        host (Optional[str], optional): The host to connect to. Defaults to 'localhost'.
    """
    user:       str
    password:   str
    port:       typing.Optional[int] = None
    host:       typing.Optional[str] = 'localhost'

    def _create_connection_string(self, name:typing.Optional[str] = None) -> str:
        """ Method for creating connection string for database with authentication."""
        connection_string = f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}"

        if self.port:
            connection_string += f":{self.port}"

        if name:
            return f"{connection_string}/{name}"

        return f"{connection_string}/{self.name}"

@dataclass(kw_only=True)
class DatabaseBase(abc.ABC):
    """ Anstract class for ORM SQLAlchemy ORM base
    
    Attributes:
        Base (Any): The base for the database. Only read. Use the base property to get the base.
        engine (Engine): A SQLAlchemy engine object
        base (Any): The base for the database.
    """

    def __post_init__(self):
        if not hasattr(self, 'Base'):
            raise AttributeError("Base attribute is not defined")

    @property
    def base(self) -> DeclarativeBase: 
        """Property for the base associated to the object.

        Only read access is allowed.
        
        Returns:
            DeclarativeBase: A SQLAlchemy base object
        """
        return self.Base

@dataclass(kw_only=True)
class DeclarativeDatabaseBase(DatabaseBase, abc.ABC):
    """ Declarative base abstract class for declarative Base 
    
    Attributes:
        Base (Any): The declarative base for the database.
        create_tables (bool, optional): If True, the tables are created when the object is instantiated. Defaults to False.
        """
    # Base typing: https://stackoverflow.com/questions/58325495/what-type-do-i-use-for-sqlalchemy-declarative-base
    Base:           DeclarativeBase
    create_tables:  bool = False

    def __post_init__(self):

        if self.create_tables:
            logger.warning(f"Creating tables for {self.name}. This may create conflicts with alembic.")
            self._create_tables()

        super().__post_init__()

    def _create_tables(self):
        """ Method for creating the all the tables from the base in the database """
        self.base.metadata.create_all(self.engine)

@dataclass(kw_only=True)
class AutoMappedDatabaseBase(DatabaseBase, abc.ABC):
    """ Automapped base abstract class for automapped Base"""

    def __post_init__(self):
        self._base_preparation()
        super().__post_init__()

    def _base_preparation(self):
        """ Method for preparing the automapped base reflecting the database schema """
        self.Base = automap_base()
        self.Base.metadata.reflect(bind=self.engine)
        self.Base.prepare()

class SQLAlchemyDatabase(Protocol):
    """ Protocol for SQLAlchemy database objects.
     
    
     """
    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        """ A SQLAlchemy engine object """
        ...

    @property
    def base(self) -> DeclarativeBase:
        """ A SQLAlchemy base object """
        ...

    @property
    def session(self) -> Session:
        """ A SQLAlchemy session object """
        ...

class InspectionMixin(SQLAlchemyDatabase):
    """Mixin for inspecting database schema
    
    Attributes:
        inspector (Inspector): A SQLAlchemy inspector object
    """

    def __post_init__(self):
        try:
            self._inspector = sqlalchemy.inspect(self.engine)
        except sqlalchemy.exc.OperationalError as e:
            logger.error(f"Could not create inspector for database {self.name}. {e}")
            raise e

    @property
    def inspector(self):
        """A SQLAlchemy inspector object"""
        return self._inspector

    def get_table_names(self) -> typing.List[str]:
        """ Method for getting the table names from the database 
        
        Returns:
            List[str]: A list of table names
        """
        return self.base.metadata.tables.keys()

    def get_database_names(self, starts_with=None, ends_with=None) -> typing.List[str]:
        """ Method for getting the database names from the the SQL server

        Args:
            starts_with (Optional[str], optional): If given, only the databases starting with the given string are returned. Defaults to None.
            ends_with (Optional[str], optional): If given, only the databases ending with the given string are returned. Defaults to None.

        Returns:
            List[str]: A list of database names
        """
        schema_list = self.inspector.get_schema_names()

        if starts_with:
            schema_list = [name for name in schema_list if name.startswith(starts_with)]

        if ends_with:
            schema_list = [name for name in schema_list if name.endswith(ends_with)]

        return schema_list

# Module API
@dataclass(kw_only=True)
class DeclarativeDatabase(AuthDatabaseConnection, DeclarativeDatabaseBase, InspectionMixin):
    """ Declarative database class for SQL databases"""
    pass

@dataclass(kw_only=True)
class DeclarativeLiteDatabase(LiteDatabaseConnection, DeclarativeDatabaseBase, InspectionMixin):
    """ Declarative database class for SQLite database"""
    pass

@dataclass(kw_only=True)
class AutoMappedDatabase(AuthDatabaseConnection, AutoMappedDatabaseBase, InspectionMixin):
    """ Automapped database class for SQL databases """
    pass

@dataclass(kw_only=True)
class AutoMappedLiteDatabase(LiteDatabaseConnection, AutoMappedDatabaseBase, InspectionMixin):
    """ Automapped database class for SQLite database """
    pass

# Base Factory