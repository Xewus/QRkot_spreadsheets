"""ORM-модель ддя таблицы 'charity_project`.
"""
import sqlalchemy as sa

from app.core import db
from app.models.base import GenericFields


class CharityProject(db.Base,  GenericFields):
    """Таблица для благотворительных проектов `charityproject`.

    ### Attrs:
    - id (int):
        Первичный ключ.
    - name (str):
        Уникальное название проекта, длина от 1 до 100.
    - description (str):
        Описание проекта.
    - full_amount (int):
        требуемая сумма больше 0.
    - invested_amount (int):
        Внесённая сумма.
        Default to 0.
    - fully_invested (bool):
        Собрана ли нужная сумма для проекта (закрыт ли проект).
        Default to False.
    - create_date (datetime):
        Дата создания проекта.
        Default to datetime.now()
    - close_date (datetime):
        Дата закрытия проекта.
    """

    __table_args__ = (
        GenericFields.__table_args__ + (sa.CheckConstraint(
            'length(name) BETWEEN 1 AND 100',
            name='invalid length of name'
        ),)
    )

    name = sa.Column(
        sa.String(100),
        unique=True,
        nullable=False
    )

    description = sa.Column(
        sa.Text,
        nullable=False
    )
