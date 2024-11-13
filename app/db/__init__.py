from contextlib import asynccontextmanager
from os import getenv

from asyncpg import Pool, create_pool
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db import models
from app.db.query import AsyncQuerier

_database_url = getenv("DATABASE_URL")
_db_pool: Pool


@asynccontextmanager
async def db_lifespan():
    global _db_pool
    _db_pool = await create_pool(dsn=_database_url, min_size=1, max_size=10)
    try:
        yield
    finally:
        await _db_pool.close()


async def get_db_querier():
    async with _db_pool.acquire() as connection:
        yield AsyncQuerier(AsyncConnection(connection))
