""" Core module containing classes for Engine+Base combinations"""

import abc
import typing
from dataclasses import dataclass, field

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

__all__ = [
    'Database',
    'LiteDatabase',
    'AutoMappedDatabase',
    'AutoMappedLiteDatabase',
]

@dataclass(kw_only=True)
class BaseDatabase(abc.ABC):
    """Base class representing minimal database connections for SQLALchemy"""
    dialect:    str
    driver:     str 
    name:       str
    # Additional connection arguments
    driver:         str = None
    echo:           bool = False
    future:         bool = True
    engine_args:    typing.Dict[str, typing.Any] = field(default_factory=dict)

    def __post_init__(self):
        connection_string: str = self._create_connection_string()

        self._engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(
            connection_string, echo=self.echo, future=self.future, **self.engine_args)

        self._session_factory = sessionmaker(self._engine)

    @property
    def session(self):
        return self._session_factory()

    @property
    def autocommit_session(self):
        return self._session_factory.begin()


    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine: sqlalchemy.engine.Engine):
        self._engine = engine

    @property
    @abc.abstractmethod
    def base(self):
        return self.Base

    @property
    def connection_string(self):
        return self._create_connection_string()

    @abc.abstractmethod
    def _create_connection_string(self) -> str:
        raise NotImplementedError

@dataclass(kw_only=True)
class LiteDatabaseMixin(BaseDatabase):
    """ Lite connection interface """

    def _create_connection_string(self) -> str:
        return f"{self.dialect}+{self.driver}:///{self.name}"

@dataclass(kw_only=True)
class AuthDatabaseMixin(BaseDatabase):
    """ Complete connection interface with user, password, host and port """
    user:       str 
    password:   str 
    port:       int = None
    host:       str = 'localhost'


    def _create_connection_string(self) -> str:
        connection_string = f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}"

        if self.port:
            connection_string += f":{self.port}"

        return f"{connection_string}/{self.name}"

@dataclass(kw_only=True)
class DeclarativeInterface:
    """ Declarative interface for database metadata """
    # Base typing: https://stackoverflow.com/questions/58325495/what-type-do-i-use-for-sqlalchemy-declarative-base
    Base:           typing.Any
    create_tables:  bool = True

    def __post_init__(self):
        super().__post_init__()

        if self.create_tables:
            self._create_tables()

    def _create_tables(self):
        self.Base.metadata.create_all(self.engine)

    @property
    def base(self):
        return self.Base

@dataclass(kw_only=True)
class AutoMappedInterface:
    """ Automapped interface for database metadada """

    def __post_init__(self):
        super().__post_init__()
        self._base_preparation()


    def _base_preparation(self):
        self.Base = automap_base()
        self.Base.metadata.reflect(bind=self.engine)
        self.Base.prepare()

    @property
    def base(self):
        return self.Base  

# Module API
@dataclass(kw_only=True)
class Database(DeclarativeInterface, AuthDatabaseMixin):
    """ Declarative database class for SQL databases"""
    pass

@dataclass(kw_only=True)
class LiteDatabase(DeclarativeInterface, LiteDatabaseMixin):
    """ Declarative database class for SQLite database"""
    pass

@dataclass(kw_only=True)
class AutoMappedDatabase(AutoMappedInterface, AuthDatabaseMixin):
    """ Automapped database class for SQL databases """
    pass

@dataclass(kw_only=True)
class AutoMappedLiteDatabase(AutoMappedInterface, LiteDatabaseMixin):
    """ Automapped database class for SQLite database """
    pass





