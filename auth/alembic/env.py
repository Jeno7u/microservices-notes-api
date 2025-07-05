import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, text
from sqlalchemy import pool, MetaData

from alembic import context

from app.models import User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = User.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


DB_URL = os.getenv("SYNC_DATABASE_URL")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DB_URL or config.get_main_option("sqlalchemy.url")
    assert url, "No database URL found in SYNC_DATABASE_URL or alembic.ini"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=config.get_main_option("version_table"),
        version_table_schema=config.get_main_option("version_table_schema")
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    section = config.get_section(config.config_ini_section)
    section["sqlalchemy.url"] = DB_URL or config.get_main_option("sqlalchemy.url")
    assert section["sqlalchemy.url"], "No DB URL found in env or alembic.ini"

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Create the notes schema if it doesn't exist
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        connection.commit()
        
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            version_table=config.get_main_option("version_table"),
            version_table_schema=config.get_main_option("version_table_schema")
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
