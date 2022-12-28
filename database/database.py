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
    echo:           bool = False
    future:         bool = True
    engine_args:    typing.Dict[str, typing.Any] = field(default_factory=dict)

    def __post_init__(self):
        self._engine: sqlalchemy.engine.Engine = self.generate_engine()
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
    def _create_connection_string(self, name:str = None) -> str:
        raise NotImplementedError

    # Engine factory methods
    def generate_engine(self, name: str = None) -> sqlalchemy.engine.Engine:
        connection_string: str = self._create_connection_string(name=name if name else self.name)
        return sqlalchemy.create_engine(connection_string, echo=self.echo, future=self.future, **self.engine_args)

    def get_engines_from_list(self, database_list: typing.List[str]) -> typing.Dict[str, sqlalchemy.engine.Engine]:
        return {name: self.generate_engine(name=name) for name in database_list}

@dataclass(kw_only=True)
class LiteDatabaseMixin(BaseDatabase):
    """ Lite connection interface """

    def _create_connection_string(self, name:str = None) -> str:
        if name:
            return f"{self.dialect}+{self.driver}:///{name}"
        return f"{self.dialect}+{self.driver}:///{self.name}"


@dataclass(kw_only=True)
class AuthDatabaseMixin(BaseDatabase):
    """ Complete connection interface with user, password, host and port """
    user:       str
    password:   str
    port:       int = None
    host:       str = 'localhost'

    def _create_connection_string(self, name:str = None) -> str:
        connection_string = f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}"

        if self.port:
            connection_string += f":{self.port}"

        if name:
            return f"{connection_string}/{name}"

        return f"{connection_string}/{self.name}"

class DatabaseBase:
    """ Class for database with SQLAlquemy base schema"""

    @property
    def base(self):
        return self.Base

@dataclass(kw_only=True)
class DeclarativeInterface(DatabaseBase):
    """ Declarative interface for database metadata """
    # Base typing: https://stackoverflow.com/questions/58325495/what-type-do-i-use-for-sqlalchemy-declarative-base
    Base:           typing.Any
    create_tables:  bool = False

    def __post_init__(self):
        super().__post_init__()

        if self.create_tables:
            self._create_tables()

    def _create_tables(self):
        self.Base.metadata.create_all(self.engine)

@dataclass(kw_only=True)
class AutoMappedInterface(DatabaseBase):
    """ Automapped interface for database metadada """

    def __post_init__(self):
        super().__post_init__()
        self._base_preparation()

    def _base_preparation(self):
        self.Base = automap_base()
        self.Base.metadata.reflect(bind=self.engine)
        self.Base.prepare()

class InspectionMixin:
    """Mixin for inspecting database schema"""

    def __post_init__(self):
        super().__post_init__()
        self._inspector = sqlalchemy.inspect(self.engine)

    @property
    def inspector(self):
        return self._inspector

    def get_table_names(self):
        return self.base.metadata.tables.keys()

    def get_database_names(self, starts_with=None, ends_with=None):
        schema_list = self.inspector.get_schema_names()

        if starts_with:
            schema_list = [name for name in schema_list if name.startswith(starts_with)]

        if ends_with:
            schema_list = [name for name in schema_list if name.endswith(ends_with)]

        return schema_list

# Module API
@dataclass(kw_only=True)
class Database(DeclarativeInterface, InspectionMixin, AuthDatabaseMixin):
    """ Declarative database class for SQL databases"""
    pass

@dataclass(kw_only=True)
class LiteDatabase(DeclarativeInterface, InspectionMixin, LiteDatabaseMixin):
    """ Declarative database class for SQLite database"""
    pass

@dataclass(kw_only=True)
class AutoMappedDatabase(AutoMappedInterface, InspectionMixin, AuthDatabaseMixin):
    """ Automapped database class for SQL databases """
    pass

@dataclass(kw_only=True)
class AutoMappedLiteDatabase(AutoMappedInterface, InspectionMixin, LiteDatabaseMixin):
    """ Automapped database class for SQLite database """
    pass