from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

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

# Base for ORM: https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.declarative_base
Base = declarative_base(metadata=meta)

# TODO: Set up a logger for this
def import_models() -> None:
    """Import models to be used in database by Base"""
    try:
        from .user import User
        from .address import Address
        from .role import Role
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

import_models()
