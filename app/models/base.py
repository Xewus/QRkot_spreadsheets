"""Базовые настройки для моделей.
"""
from datetime import datetime

import sqlalchemy as sa


class GenericFields:
    """Сборник общих полей для моделей.

    ### Attrs:
    - full_amount (int):
        Больше 0.
    - invested_amount (int):
        Default to 0.
    - fully_invested (bool):
        Default to False.
    - create_date (datetime):
        Дата создания.
        Default to datetime.now()
    - close_date (datetime):
        Дата закрытия.
    """

    __table_args__ = (
        sa.CheckConstraint(
            'full_amount > 0',
            name='full_amount is not positive'
        ),
        sa.CheckConstraint(
            'invested_amount >= 0',
            name='invested_amount is negative'
        ),
        sa.CheckConstraint(
            'invested_amount <= full_amount',
            name='invested_amount is more than full_amount'
        ),
        # sa.CheckConstraint(
        #     'create_date <= close_date',
        #     name='close_date is earlier than create_date'
        # )
    )

    full_amount = sa.Column(
        sa.Integer,
        nullable=False
    )
    invested_amount = sa.Column(
        sa.Integer,
        nullable=False,
        default=0
    )
    fully_invested = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False,
        index=True
    )
    create_date = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.now
    )
    close_date = sa.Column(
        sa.DateTime,
        nullable=True
    )
