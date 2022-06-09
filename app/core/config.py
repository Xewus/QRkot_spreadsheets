"""Начальные настройки приложения.
"""
from typing import Union

import pydantic as pd


class Settings(pd.BaseSettings):
    """Настройки приложения.
    """
    path: str
    debug: bool = False
    echo: Union[None, bool] = None
    app_title: str = 'Project'
    description: str = 'Really cool project'
    version: str = '0.0.0'
    database_url: str = 'sqlite+aiosqlite:///./test_project.db'
    secret: str = 'reaLLy L0nG $tr1nG'
    first_superuser_email: Union[None, pd.EmailStr] = None
    first_superuser_password: Union[None, str] = None

    class Config:
        env_file = '.env'


settings = Settings()

# Для просмотра SQL-запросов в терминале
if settings.debug and settings.echo is None:
    settings.echo = True
