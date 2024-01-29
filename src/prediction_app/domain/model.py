from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class StatusEnum(str, Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'


class PredictedClassEnum(str, Enum):
    NORMAL_DRIVING = 'NORMAL_DRIVING'
    TEXTING_RIGHT = 'TEXTING_RIGHT'
    TALKING_ON_THE_PHONE_RIGHT = 'TALKING_ON_THE_PHONE_RIGHT'
    TEXTING_LEFT = 'TEXTING_LEFT'
    TALKING_ON_THE_PHONE_LEFT = 'TALKING_ON_THE_PHONE_LEFT'
    OPERATING_THE_RADIO = 'OPERATING_THE_RADIO'
    DRINKING = 'DRINKING'
    REACHING_BEHIND = 'REACHING_BEHIND'
    HAIR_AND_MAKEUP = 'HAIR_AND_MAKEUP'
    TALKING_TO_PASSENGER = 'TALKING_TO_PASSENGER'


class Prediction(BaseModel):
    id: UUID
    status: StatusEnum
    prediction_class: Optional[PredictedClassEnum] = None
    prediction_probability: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class PredictionOptional(BaseModel):
    id: UUID
    status: Optional[StatusEnum]
    prediction_class: Optional[PredictedClassEnum] = None
    prediction_probability: Optional[float] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


mapping_class_to_enum = {
    0: 'NORMAL_DRIVING',
    1: 'TEXTING_RIGHT',
    2: 'TALKING_ON_THE_PHONE_RIGHT',
    3: 'TEXTING_LEFT',
    4: 'TALKING_ON_THE_PHONE_LEFT',
    5: 'OPERATING_THE_RADIO',
    6: 'DRINKING',
    7: 'REACHING_BEHIND',
    8: 'HAIR_AND_MAKEUP',
    9: 'TALKING_TO_PASSENGER',
}
