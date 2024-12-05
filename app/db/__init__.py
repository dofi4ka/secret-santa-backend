from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator, AsyncContextManager, TypeAlias

from asyncpg import Pool, create_pool
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.models import *
from app.db.query import *

_DATABASE_URL = getenv("DATABASE_URL")
_db_pool: Pool
QuerierType: TypeAlias = AsyncQuerier


@asynccontextmanager
async def db_lifespan():
    global _db_pool
    _db_pool = await create_pool(dsn=_DATABASE_URL, min_size=1, max_size=10)
    try:
        yield
    finally:
        await _db_pool.close()


async def _db_querier_core() -> AsyncGenerator[QuerierType, None]:
    async with _db_pool.acquire() as connection:
        yield AsyncQuerier(AsyncConnection(connection))


# for FastAPI injection system
async def db_querier_gen() -> AsyncGenerator[QuerierType, None]:
    async for querier in _db_querier_core():
        yield querier


# for any other manual use
def db_querier_context() -> AsyncContextManager[QuerierType]:
    return asynccontextmanager(_db_querier_core)()
