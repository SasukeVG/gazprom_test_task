from typing import List
from uuid import UUID

import asyncpg
from fastapi import HTTPException

from prediction_app.domain.model import Prediction, PredictionOptional, mapping_class_to_enum


async def create_status_enum(connection: asyncpg.Connection):
    try:
        await connection.execute("CREATE TYPE status AS ENUM ('PENDING', 'SUCCESS', 'FAILURE');")
    except asyncpg.exceptions.DuplicateObjectError:
        pass


async def create_class_enum(connection: asyncpg.Connection):
    try:
        await connection.execute(
            "CREATE TYPE predicted_class AS ENUM ('NORMAL_DRIVING', 'TEXTING_RIGHT', 'TALKING_ON_THE_PHONE_RIGHT', 'TEXTING_LEFT', 'TALKING_ON_THE_PHONE_LEFT', 'OPERATING_THE_RADIO', 'DRINKING', 'REACHING_BEHIND', 'HAIR_AND_MAKEUP', 'TALKING_TO_PASSENGER');")
    except asyncpg.exceptions.DuplicateObjectError:
        pass


async def create_prediction_table(connection: asyncpg.Connection):
    await connection.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction (
            id uuid PRIMARY KEY,
            status status NOT NULL,
            prediction_class predicted_class NULL,
            prediction_probability float8 NULL,
            created_at timestamp without time zone NOT NULL DEFAULT now(),
            updated_at timestamp without time zone NOT NULL DEFAULT now()
        )
        """
    )


async def create_tables(connection: asyncpg.Connection):
    await create_status_enum(connection)
    await create_class_enum(connection)
    await create_prediction_table(connection)


async def insert_info_prediction_table(connection: asyncpg.Connection, uuid: UUID):
    await connection.execute(
        """
        INSERT INTO prediction (id, status)
        VALUES ($1, 'PENDING')
        """,
        uuid
    )


async def update_info_prediction_table(connection: asyncpg.Connection, uuid: UUID, prediction_class: int,
                                       prediction_probability: float):
    prediction_enum = mapping_class_to_enum[prediction_class]
    await connection.execute(
        """
        UPDATE prediction
        SET status = 'SUCCESS',
            prediction_class = $2,
            prediction_probability = $3,
            updated_at = now()
        WHERE id = $1
        """,
        uuid,
        prediction_enum,
        prediction_probability
    )


async def get_prediction(connection: asyncpg.Connection, uuid: UUID) -> Prediction:
    row = await connection.fetchrow(
        """
        SELECT id, status, prediction_class, prediction_probability, created_at, updated_at
        FROM prediction
        WHERE id = $1
        """,
        uuid
    )
    if not row:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return Prediction(**row)


async def create_prediction(connection: asyncpg.Connection, prediction: Prediction):
    await connection.execute(
        """
        INSERT INTO prediction (id, status, prediction_class, prediction_probability, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        """,
        prediction.id,
        prediction.status,
        prediction.prediction_class,
        prediction.prediction_probability,
        prediction.created_at.replace(tzinfo=None),
        prediction.updated_at.replace(tzinfo=None),
    )


async def update_prediction(connection: asyncpg.Connection, prediction: PredictionOptional) -> bool:
    set_clauses = []
    values = []

    if prediction.status is not None:
        set_clauses.append("status = $1")
        values.append(prediction.status)

    if prediction.prediction_class is not None:
        set_clauses.append("prediction_class = $" + str(len(values) + 1))
        values.append(prediction.prediction_class)

    if prediction.prediction_probability is not None:
        set_clauses.append("prediction_probability = $" + str(len(values) + 1))
        values.append(prediction.prediction_probability)

    if prediction.created_at is not None:
        set_clauses.append("created_at = $" + str(len(values) + 1))
        values.append(prediction.created_at.replace(tzinfo=None))

    if prediction.updated_at is not None:
        set_clauses.append("updated_at = $" + str(len(values) + 1))
        values.append(prediction.updated_at.replace(tzinfo=None))

    query = """
    UPDATE prediction
    SET {}
    WHERE id = ${}
    """.format(", ".join(set_clauses), len(values) + 1)

    values.append(prediction.id)

    result = await connection.execute(query, *values)
    return "UPDATE 1" in result


async def delete_prediction(connection: asyncpg.Connection, id_: UUID) -> bool:
    result = await connection.execute(
        """
        DELETE FROM prediction
        WHERE id = $1
        """,
        id_
    )
    return "DELETE 1" in result


async def fetch_predictions(connection: asyncpg.Connection, offset: int, limit: int) -> List[Prediction]:
    rows = await connection.fetch(
        """
        SELECT id, status, prediction_class, prediction_probability, created_at, updated_at
        FROM prediction
        ORDER BY created_at DESC
        OFFSET $1 LIMIT $2
        """,
        offset,
        limit
    )
    print(rows)
    return [Prediction(**row) for row in rows]
