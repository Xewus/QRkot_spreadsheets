"""Операции CRUD для модели `Donation`.
"""
from typing import List

from pydantic import UUID4

from app import models
from app.core import db
from app.crud.base import CRUDBase


class CRUDDonation(CRUDBase):
    """Класс с запросами к таблице `donation`.
    """

    async def get_my_donations(
        self,
        user_id: UUID4,
        session: db.AsyncSession
    ) -> List[models.Donation]:
        """Получает список пожертвований указанного пользователя.

        ### Args:
        - user_id (UUID4):
            `id` пользователя.
        - session (db.AsyncSession):
            Объект сессии с БД.

        ### Returns:
        - List[models.Donation]:
            Список пожертвований указанного пользователя.
        """
        return await super().get_by_field(
            required_field='user_id',
            value=user_id,
            session=session,
            one_obj=False
        )


donation_crud = CRUDDonation(models.Donation)
