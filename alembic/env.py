import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Ongeza njia (path) ya project yako ili Alembic iweze kuona folda ya app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Import Base yako ya SQLAlchemy na faili la kusoma .env kama lipo
from app.db.base import Base  # Badilisha iendane na pale ulipoweka Base yako
from app.core.config import settings  # Au unaweza kutumia os.environ kama unatumia python-dotenv

# Hapa ndipo Alembic inasoma metadata ya tables zako
target_metadata = Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- SEMUU MUHIMU: HAPA NDIPO TUNAPOBADILISHA URL ---
# Hapa tunamwambia Alembic achukue DATABASE_URL kutoka kwenye settings au .env yako ya Render
db_url = getattr(settings, "DATABASE_URL", None)
if not db_url:
    db_url = os.getenv("DATABASE_URL")

if db_url:
    # Kama inaanza na postgres:// (mara nyingi Render inatoa hivi), ibadilishe iwe postgresql:// ili isomeke vizuri na SQLAlchemy
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    config.set_main_option("sqlalchemy.url", db_url)
# ----------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_online() # au offline kutegemeana na mazingira
else:
    run_migrations_online()