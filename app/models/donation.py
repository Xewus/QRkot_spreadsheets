"""ORM-модель ддя таблицы 'donation`.
"""
import fastapi_users_db_sqlalchemy as fa_u_sa
import sqlalchemy as sa

from app.core import db
from app.models.base import GenericFields


class Donation(db.Base, GenericFields):
    """Таблица для пожертвований `donation`.

    ### Attrs:
    - id (int):
        Первичный ключ.
    - user_id (str):
        Foreign Key. id пользователя, сделавшего пожертвование.
    - comment (None | str):
        Необязательный текст комментария.
    - full_amount (int):
        Сумма пожертвования. Больше 0.
    - invested_amount (int):
        Сумма из пожертвования, распределенная по проектам.
        Defaults to 0.
    - fully_invested (bool):
        Все ли деньги из пожертвования были распределены.
        Defaults to False.
    - create_date (datetime):
        Дата пожертвования.
        Default to datetime.now()
    - close_date (datetime):
        Дата, когда вся сумма пожертвования была распределена.
    """

    user_id = sa.Column(
        fa_u_sa.GUID,
        sa.ForeignKey('user.id')
    )
    comment = sa.Column(
        sa.Text,
        nullable=True
    )
