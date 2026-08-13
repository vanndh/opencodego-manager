"""SQLAlchemy 2.0 async engine + session factory (SQLite WAL)."""

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.app import DB_PATH


class Base(DeclarativeBase):
    pass


def make_engine(db_path: Path = DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(
        url,
        connect_args={"timeout": 30},
        pool_pre_ping=True,
    )
    return engine


engine = make_engine()
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Создать таблицы. Миграции — отдельный лёгкий слой (см. migrations)."""
    from storage import models  # noqa: F401 — регистрация таблиц в Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with SessionLocal() as session:
        yield session
