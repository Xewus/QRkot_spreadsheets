"""Операции CRUD для модели `CharityProject`.
"""
from app import models
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    """Класс с запросами к таблице `charityproject`.
    """


charity_projects_crud = CRUDCharityProject(models.CharityProject)
