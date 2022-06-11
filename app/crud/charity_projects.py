"""Операции CRUD для модели `CharityProject`.
"""
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud.base import CRUDBase
from app.services import utils


class CRUDCharityProject(CRUDBase):
    """Класс с запросами к таблице `charityproject`.
    """
    async def get_project_by_completion_rate(
        self,
        session: AsyncSession,
        reverse: bool = False
    ) -> Union[None, List]:
        """Получает список закрытых проектов сортированый по
        разнице между временем открытия и закрытия.

        ### Args:
        - session (AsyncSession):
            Объект сессии с БД.
        - reverse (bool):
            Направлени сортированного списка.
            По умолчанию начинается с наименьшего.
            Default to False

        ### Returns:
        - List[ChatityProject]:
            Осортированный список проектов.
        """
        closed_projects = await self.get_by_field(
            required_field='fully_invested',
            value=True,
            session=session,
            one_obj=False
        )
        closed_projects.sort(
            key=utils.sort_by_timedelta,
            reverse=reverse
        )
        return closed_projects


charity_projects_crud = CRUDCharityProject(models.CharityProject)
