from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Metadata for ORM: https://docs.sqlalchemy.org/en/14/core/metadata.html
# Naming convention: https://alembic.sqlalchemy.org/en/latest/naming.html
meta: MetaData = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

# Base for ORM: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping
class Base(DeclarativeBase):
    """Base class for ORM."""
    metadata = meta

def create_declarative_base():
    """Create a declarative base."""

    class Base(DeclarativeBase):
        """Base class for ORM."""
        metadata = meta

    # Deferring the import of the models to avoid circular imports
    from sqltoolbox.models import user
    from sqltoolbox.models import role
    from sqltoolbox.models import address
        
    return Base