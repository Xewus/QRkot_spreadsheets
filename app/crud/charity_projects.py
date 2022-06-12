"""Операции CRUD для модели `CharityProject`.
"""
from typing import List, Union

from sqlalchemy import asc, desc, select

from app.core import db
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс с запросами к таблице `charityproject`.
    """
    async def get_project_by_completion_rate(
        self,
        session: db.AsyncSession,
        reverse: bool = False
    ) -> Union[None, List]:
        """Получает список закрытых проектов сортированый по
        разнице между временем открытия и закрытия.

        ### Args:
        - session (AsyncSession):
            Объект сессии с БД.
        - reverse (bool):
            Направлениt сортированного списка.
            По умолчанию начинается с наименьшего.
            Default to False

        ### Returns:
        - List[ChatityProject]:
            Оnсортированный список проектов.
        """
        query = select(
            CharityProject.name,
            CharityProject.description,
            (
                db.datetime_func(CharityProject.close_date) -
                db.datetime_func(CharityProject.create_date)
            ).label('lifetime')
        )
        query = (
            query.order_by(asc('lifetime')),
            query.order_by(desc('lifetime'))
        )[reverse]

        closed_projects = await session.execute(query)

        return closed_projects.all()


charity_projects_crud = CRUDCharityProject(CharityProject)
