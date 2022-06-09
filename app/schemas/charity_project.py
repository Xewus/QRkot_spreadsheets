"""Схемы регламентирующие обмен данными для работы с моделью `CharityProject`.
"""
from datetime import datetime
from typing import Union

from pydantic import (
    BaseModel,
    Extra,
    Field,
    NonNegativeInt,
    PositiveInt,
    root_validator
)

from app.services import utils


class CharityProjectBaseSchema(BaseModel):
    """Базовый класс схем данных для работы с `ChrityProject`.

    - name (int, optional):
        Название проекта. Длина от 1 до 100.
    - description (int, optional):
        Описание проекта.
    - full_amount (int, optional):
        Необходимая сумма для закрытия проекта. Больше 0.
    """
    name: Union[None, str] = Field(
        None,
        example='Очень важный проект для котов.',
        min_length=1,
        max_length=100
    )
    description: Union[None, str] = Field(
        None,
        example='Собираем немного тысяч денег для Мурзика!',
        min_length=1
    )
    full_amount: Union[None, PositiveInt] = Field(
        None,
        example=5791
    )

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBaseSchema):
    """Схема данных для создания нового благотворительного проекта.

    ### Attrs:
    - name (str):
        Название проекта. Длина от 1 до 100.
    - description (str):
        Описание проекта.
    - full_amount (int):
        Необходимая сумма для закрытия проекта. Больше 0.
    """
    name: str = Field(
        ...,
        example='Очень важный проект для котов.',
        min_length=1,
        max_length=100
    )
    description: str = Field(
        ...,
        example='Собираем немного тысяч денег для Мурзика!',
        min_length=1
    )
    full_amount: PositiveInt = Field(
        ...,
        example=5791
    )


class CharityProjectUpdate(CharityProjectBaseSchema):
    """Схема данных для обновления благотворительного проекта.

    ### Attrs:
    - name (int, optional):
        Название проекта. Длина от 1 до 100.
    - description (int, optional):
        Описание проекта.
    - full_amount (int, optional):
        Необходимая сумма для закрытия проекта. Больше 0.
    """
    pass


class CharityProjectResponse(CharityProjectCreate):
    """Схема данных возвращаемых в ответе.

    ### Attrs:
    - name (int):
        Название проекта. Длина от 1 до 100.
    - description (str):
        Описание проекта.
    - full_amount (int):
        Необходимая сумма для закрытия проекта. Больше 0.
    - id (int):
        `id` проекта.
    - invested_amount (int):
        Количество средств, внсённых в проект.
    - fully_invested (bool):
        Проинвестирован ли проект полностью.
    - create_date (datetime):
        Дата создания проекта.
    - close_date (None, datetime):
        Дата закрытия проекта.
    """
    id: PositiveInt = Field(
        ...,
        example=17
    )
    invested_amount: NonNegativeInt = Field(
        ...,
        example=134
    )
    fully_invested: bool = Field(
        ...,
        example=True
    )
    create_date: datetime = Field(
        ...,
        example='2022-05-28T16:39:33'
    )
    close_date: Union[None, datetime] = Field(
        None,
        example='2022-06-15T16:39:13'
    )

    class Config:
        orm_mode = True

    @root_validator
    def normalize_datetime(cls, values: dict) -> dict:
        return utils.normalize_datetime(
            values=values
        )
