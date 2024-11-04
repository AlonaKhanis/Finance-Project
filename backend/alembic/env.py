from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app import db 
from app.models import *  
from dotenv import load_dotenv


load_dotenv()

fileConfig(context.config.config_file_name)
env = os.getenv('FLASK_ENV')

# Set the SQLAlchemy URL from the environment variable
if env == 'development':
    context.config.set_main_option('sqlalchemy.url', 'sqlite:///instance/dev.db')
elif env == 'testing':
    context.config.set_main_option('sqlalchemy.url', 'sqlite:///:memory:')
else:
    context.config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

target_metadata = db.Model.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Run the appropriate migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
