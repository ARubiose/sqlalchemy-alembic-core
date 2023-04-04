import copy
import logging
from logging.config import fileConfig

from alembic import context

from sqltoolbox.config import database

USE_TWOPHASE = False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# gather section names referring to different
# databases.  These are named "engine1", "engine2"
# in the sample .ini file.
db_names = database.get_database_names(starts_with="database")

# add your model's MetaData objects here
# for 'autogenerate' support.  These must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a "copy" of
# a MetaData is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# } 
# target_metadata = {name: copy.copy(database.base.metadata) for name in db_names}
target_metadata = database.base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# HOOKS


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines = {}
    for name in db_names:
        engines[name] = rec = {}
        rec["url"] = context.config.get_section_option(name, "sqlalchemy.url")

    for name, rec in engines.items():
        logger.info("Migrating database %s" % name)
        file_ = "%s.sql" % name
        logger.info("Writing output to %s" % file_)
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=target_metadata.get(name),
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines_data = dict()

    for name, engine in database.get_engines_from_list(db_names).items():
        engines_data[name] = engine_dict = dict(engine=engine)
        engine_dict["connection"] = connection = engine.connect()
        engine_dict["transaction"] = connection.begin_twophase() if USE_TWOPHASE else connection.begin()

    try:
        for name, engine_dict in engines_data.items():
            logger.info("Migrating database %s" % name)
            context.configure(
                connection=engine_dict.get("connection"),
                upgrade_token=f"{name}_upgrades",
                downgrade_token=f"{name}_downgrades",
                target_metadata=target_metadata
            )
            context.run_migrations(engine_name=name)

        if USE_TWOPHASE:
            for engine_dict in engines_data.values():
                engine_dict["transaction"].prepare()

        for engine_dict in engines_data.values():
            engine_dict["transaction"].commit()

    except Exception as e:
        logger.error("Error: %s" % e)
        for engine_dict in engines_data.values():
            engine_dict["transaction"].rollback()
        raise
    finally:
        for engine_dict in engines_data.values():
            engine_dict["connection"].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
