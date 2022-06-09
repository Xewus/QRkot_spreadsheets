"""Операции CRUD для модели `CharityProject`.
"""
from typing import Any, List, Union

from app import models, schemas
from app.core import db
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    """Класс с запросами к таблице `charityproject`.
    """


charity_projects_crud = CRUDCharityProject(models.CharityProject)
