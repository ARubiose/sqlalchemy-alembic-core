""" Core module containing classes for Engine+Base combinations"""

import typing
from dataclasses import dataclass, field

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

__all__ = [
    'DeclarativeDatabase',
    'DeclarativeLiteDatabase',
    'AutoMappedDatabase',
    'AutoMappedLiteDatabase'
]

@dataclass(kw_only=True)
class AbstractDatabase:
    """Base class representing minimal database connections for SQLALchemy"""
    dialect:    str
    name:       str
    # Additional connection arguments
    driver:         str = None
    echo:           bool = False
    future:         bool = True
    create_tables:  bool = True
    engine_args:    typing.Dict[str, typing.Any] = field(default_factory=dict)

class SessionMixin:
    """ Session factory mixin """
    @property
    def session(self):
        return self._session_factory()

    @property
    def autocommit_session(self):
        return self._session_factory.begin()


@dataclass(kw_only=True)
class DeclarativeInterface(AbstractDatabase, SessionMixin):
    """ Declarative interface for database metadata """
    # Base typing: https://stackoverflow.com/questions/58325495/what-type-do-i-use-for-sqlalchemy-declarative-base
    Base:       typing.Any

    def __post_init__(self):
        connection_string: str = self._create_connection_string()
        self.engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(
            connection_string, echo=self.echo, future=self.future, **self.engine_args)
        self._session_factory = sessionmaker(self.engine)

        if self.create_tables:
            self._create_tables()

    @property
    def base(self):
        return self.Base

    def _create_tables(self):
        self.Base.metadata.create_all(self.engine)

@dataclass(kw_only=True)
class AutoMappedInterface(AbstractDatabase, SessionMixin):
    """ Automapped interface for database metadada """

    def __post_init__(self):
        connection_string: str = self._create_connection_string()

        self.engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(
            connection_string, echo=self.echo, future=self.future, **self.engine_args)

        self._base_preparation()

        self._session_factory = sessionmaker(self.engine)

    def _base_preparation(self):
        self.Base = automap_base()
        self.Base.metadata.reflect(bind=self.engine)
        self.Base.prepare()

    @property
    def base(self):
        return self.Base    

@dataclass(kw_only=True)
class LiteDatabaseInterface(AbstractDatabase):
    """ Lite connection interface """

    def _create_connection_string(self) -> str:
        return f"{self.dialect}+{self.driver}:///{self.name}"

@dataclass(kw_only=True)
class DatabaseInterface(AbstractDatabase):
    """ Complete connection interface """
    user:       str 
    password:   str 
    port:       int = None
    host:       str = 'localhost'


    def _create_connection_string(self) -> str:
        connection_string = f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}"

        if self.port:
            connection_string += f":{self.port}"

        return f"{connection_string}/{self.name}"

# Module API
class DeclarativeDatabase(DeclarativeInterface, DatabaseInterface):
    """ Declarative database class for SQL databases"""
    pass

class DeclarativeLiteDatabase(DeclarativeInterface, LiteDatabaseInterface):
    """ Declarative database class for SQLite database"""
    pass

class AutoMappedDatabase(AutoMappedInterface, DatabaseInterface):
    """ Automapped database class for SQL databases """
    pass

class AutoMappedLiteDatabase(AutoMappedInterface, LiteDatabaseInterface):
    """ Automapped database class for SQLite database """
    pass





