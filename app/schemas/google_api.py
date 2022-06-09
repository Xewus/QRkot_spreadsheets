"""Схемы регламентирующие обмен данными c `Google API`.
"""
from typing import Dict, List

from pydantic import BaseModel, Extra, Field


class GoogleAPIBaseSchema(BaseModel):
    reservations: List[Dict[str, str]] = Field(
        ...,
        example=[
            {
                'name': 'Для помощи белым котам',
                'time_spent': '1 day, 12:27:54.123456',
                'description': 'Будем из одиноких белых котов делать других'
            }
        ]
    )

    class Config:
        extra = Extra.forbid


class GoogleAPIResponseSchema(GoogleAPIBaseSchema):
    ...
