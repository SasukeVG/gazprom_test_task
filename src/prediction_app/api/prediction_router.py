from typing import Optional, List
from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from prediction_app.db.connector import get_db_connection_
from prediction_app.db.model import get_prediction, create_prediction, update_prediction, delete_prediction, fetch_predictions
from prediction_app.domain.model import Prediction, PredictionOptional

"""
create table public.prediction
(
    id                     uuid                    not null
        primary key,
    status                 status                  not null,
    prediction_class       predicted_class,
    prediction_probability double precision,
    created_at             timestamp default now() not null,
    updated_at             timestamp default now() not null
);
"""

router = APIRouter(
    prefix='/prediction',
    tags=['prediction'],
)


@router.get(
    '/{id}',
    response_model=Prediction,
    responses={
        404: {"description": "Prediction not found"},
        200: {"description": "Prediction found"},
    }
)
async def read_prediction(
    id: UUID,
    db_connection=Depends(get_db_connection_),
) -> Optional[Prediction]:
    return await get_prediction(db_connection, id)


@router.post(
    '/',
    status_code=HTTP_201_CREATED,
    responses={
        409: {"description": "Unique constraint violated"},
        201: {"description": "Prediction created"},
    }
)
async def create_prediction_(
    message: Prediction,
    db_connection=Depends(get_db_connection_),
) -> int:
    try:
        await create_prediction(db_connection, message)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail=f"Unique constraint violated")
    return HTTP_201_CREATED


@router.patch(
    '/',
    status_code=HTTP_200_OK,
    responses={
        404: {"description": "Prediction not found"},
        200: {"description": "Prediction updated"},
    }
)
async def update_prediction_(
    message: PredictionOptional,
    db_connection=Depends(get_db_connection_),
) -> int:
    updated = await update_prediction(db_connection, message)
    if not updated:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return HTTP_200_OK


@router.delete(
    '/{id}',
    status_code=HTTP_200_OK,
    responses={
        404: {"description": "Prediction not found"},
        200: {"description": "Prediction deleted"},
    }
)
async def delete_prediction_(
    id: UUID,
    db_connection=Depends(get_db_connection_),
):
    deleted = await delete_prediction(db_connection, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return HTTP_200_OK


predictions_router = APIRouter(
    prefix='/predictions',
    tags=['prediction'],
)


@predictions_router.get('/')
async def get_all_predictions(
    db_connection=Depends(get_db_connection_),
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
) -> List[Prediction]:
    return await fetch_predictions(db_connection, offset, limit)
