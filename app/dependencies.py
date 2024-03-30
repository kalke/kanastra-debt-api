from contextlib import asynccontextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import config

async_engine = create_async_engine(config.DATABASE_URL, echo=True)
AsyncLocalSession = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_db():
    async with AsyncLocalSession() as session:
        try:
            yield session
        finally:
            await session.close()
