"""Набор функций, выполняемых перед запуском приложения.
"""
import contextlib

from fastapi_users.manager import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
):
    """Создаёт пользователя.

    Если пользователь с аналогичным идентификатором уже
    существует - не делает ничего.

    ### Args:
    - email (EmailStr):
        Электронная почта пользователя.
    - password (str):
        Пароль для входа в аккаунт.
    - is_superuser (bool, optional):
        Установить ли статус `привелегированного` пользлвателя.
        Defaults to False.
    """
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Создаёт суперпользователя при запуске приложения,
    если в настройках приложения указано такое требование.
    """
    if (
        settings.first_superuser_email is not None and
        settings.first_superuser_password is not None
    ):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
