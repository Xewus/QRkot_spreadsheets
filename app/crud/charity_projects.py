"""Операции CRUD для модели `CharityProject`.
"""
from datetime import timedelta
from sqlalchemy import select, func, subquery

from app import models, schemas
from app.core import db
from app.crud.base import CRUDBase
from app.services import utils


class CRUDCharityProject(CRUDBase):
    """Класс с запросами к таблице `charityproject`.
    """
    async def get_projects_by_closing_speed(
        self,
        session: db.AsyncSession
    ) -> schemas.GoogleAPIBaseSchema:
        charity_projects = await session.scalars(
            select(
                models.CharityProject
            ).where(
                models.CharityProject.fully_invested.is_(True)
            )
        )
        charity_projects = charity_projects.all()

        charity_projects.sort(key=utils.sort_by_timdelta)
        return charity_projects


charity_projects_crud = CRUDCharityProject(models.CharityProject)
