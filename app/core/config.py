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
    # for auto_create first superuser
    first_superuser_email: Union[None, pd.EmailStr] = None
    first_superuser_password: Union[None, str] =      None
    # for Google API
    type_: Union[None, str] =                         None
    project_id: Union[None, str] =                    None
    private_key_id: Union[None, str] =                None
    private_key: Union[None, str] =                   None
    client_email: Union[None, str] =                  None
    client_id: Union[None, str] =                     None
    auth_uri: Union[None, str] =                      None
    token_uri: Union[None, str] =                     None
    auth_provider_x509_cert_url: Union[None, str] =   None
    client_x509_cert_url: Union[None, str] =          None
    email_user: Union[None, str] =                    None

    class Config:
        env_file = '.env'


settings = Settings()

# Для просмотра SQL-запросов в терминале
if settings.debug and settings.echo is None:
    settings.echo = True
