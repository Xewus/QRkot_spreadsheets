"""Импорты класса Base и всех моделей для Alembic.
"""
from app.core.db import Base  # noqa
from app.models import (      # noqa
    CharityProject,
    Donation,
    UserTable
)
