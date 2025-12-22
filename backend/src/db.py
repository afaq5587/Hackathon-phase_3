"""
Database connection module for Phase 3 Todo Chatbot.

Provides async database connectivity to Neon PostgreSQL using SQLModel and asyncpg.
Per Constitution Principle II: Stateless Architecture - no connection state persists.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import get_settings


def get_async_engine():
    """
    Create async database engine for Neon PostgreSQL.

    Converts postgresql:// to postgresql+asyncpg:// for async support.
    """
    settings = get_settings()
    database_url = settings.database_url

    # Handle SQLite
    if database_url.startswith("sqlite"):
        # For SQLModel + aiosqlite, we need sqlite+aiosqlite://
        if not database_url.startswith("sqlite+aiosqlite://"):
            database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        
        return create_async_engine(
            database_url,
            echo=settings.debug,
            # SQLite doesn't support some pooling options the same way as Postgres
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
        )

    # Convert standard PostgreSQL URL to async driver URL
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Strip sslmode=require which is not supported by asyncpg in URL
    if "sslmode=" in database_url:
        import re
        database_url = re.sub(r"[?&]sslmode=[^&]+", "", database_url)

    return create_async_engine(
        database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"ssl": True} if "neon.tech" in database_url else {},
    )


# Create engine instance
engine = get_async_engine()

# Async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """
    Initialize database tables.

    Creates all tables defined by SQLModel models.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """
    Close database connections.

    Should be called on application shutdown.
    """
    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session as context manager.

    Usage:
        async with get_session() as session:
            result = await session.execute(query)

    Automatically handles commit/rollback on exit.
    """
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for FastAPI routes.

    Usage:
        @app.get("/")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with get_session() as session:
        yield session
