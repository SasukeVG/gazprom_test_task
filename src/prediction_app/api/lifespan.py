from contextlib import asynccontextmanager

from fastapi import FastAPI

from prediction_app.db.connector import get_db_connection
from prediction_app.db.model import create_tables

model = {}


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    async with get_db_connection() as db_connection:
        await create_tables(db_connection)

    print("Starting application")

    yield

    model.clear()
    print("Stopping application")
