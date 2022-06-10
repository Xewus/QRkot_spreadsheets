"""Схемы регламентирующие обмен данными для работы с моделью `Donation`.
"""
from datetime import datetime
from typing import Union

from pydantic import (UUID4, BaseModel, Extra, Field, NonNegativeInt,
                      PositiveInt, root_validator)

from app.services import utils


class DonationBaseSchema(BaseModel):
    """Базовый класс схем данных для работы с `Donation`.

    ### Attrs:
    - full_amount:
        Сумма пожертврвания. Больше 0.
    - comment (str, optional):
        Комментарий к пожертвованию.
    """
    full_amount: PositiveInt = Field(
        ...,
        example=591
    )
    comment: Union[None, str] = Field(
        None,
        example='Очень хочу помочь Вашему проекту.'
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBaseSchema):
    """Схема данных для создания нового пожертвования.

    ### Attrs:
    - full_amount:
        Необходимая сумма для закрытия проекта. Больше 0.
    - comment (str, optional):
        Комментарий к пожертвованию.
    """
    pass


class DonationShortResponse(DonationBaseSchema):
    """Короткая схема данных для ответа.

    ### Attrs:
    - full_amount:
        Сумма пожертврвания. Больше 0.
    - comment (str, optional):
        Комментарий к пожертвованию.
    - id (int):
        `id` пожертвования.
    - create_date (datetime):
        Дата пожертвования.
    """
    id: PositiveInt = Field(
        ...,
        example=42
    )
    create_date: datetime = Field(
        ...,
        example='2022-05-28T16:39:33'
    )

    class Config:
        orm_mode = True

    @root_validator
    def normalize_datetime(cls, values: dict) -> dict:
        return utils.normalize_datetime(
            values=values
        )


class DonationLongResponse(DonationShortResponse):
    """Короткая схема данных для ответа.

    ### Attrs:
    - full_amount:
       Сумма пожертврвания. Больше 0.
    - comment (str, optional):
        Комментарий к пожертвованию.
    - id (int):
        `id` пожертвования.
    - create_date (datetime):
        Дата пожертвования.
    - user_id (UUID4):
        `id` пользователя, сделавшего пожертвование.
    - invested_amount (int):
        Сумма из пожертвования, распределённая по проектам.
    - fully_invested (bool):
        Распределены ли все средства из пожертвования.
    - close_date (None, datetime):
        Дата, когда вся сумма пожкертвования была рапсределена.
    """
    user_id: UUID4 = Field(
        ...,
        example='6cc376e0-1c89-48ee-8ab9-9541ec216b94'
    )
    invested_amount: NonNegativeInt = Field(
        ...,
        example=591
    )
    fully_invested: bool = Field(
        ...,
        example=True
    )
    close_date: Union[None, datetime] = Field(
        None,
        example='2022-05-28T16:39:33'
    )
