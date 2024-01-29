from contextlib import asynccontextmanager

import asyncpg

from prediction_app.db.config import database_config


class Database:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                user=database_config.USER,
                password=database_config.PASSWORD,
                host=database_config.HOST,
                port=database_config.PORT,
                database=database_config.DB_NAME,
            )
        return cls._pool

    @asynccontextmanager
    async def get_connection(self):
        pool = await self.get_pool()
        async with pool.acquire() as connection:
            yield connection


database = Database()


async def get_db_connection_():
    async with database.get_connection() as connection:
        yield connection


get_db_connection = asynccontextmanager(get_db_connection_)
