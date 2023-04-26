"""Настройки для работы с объектами `User`.
"""
from typing import Union

import fastapi as fa
import fastapi_users as fa_u
import fastapi_users.authentication as auth
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app import models, schemas
from app.core import config, db
from app.services import constants as const


async def get_user_db(
    session: db.AsyncSession = fa.Depends(db.get_async_session)
):
    """Генератор подключений к таблице `user` в БД.

    ### Args:
    - session (db.AsyncSession, optional):
        Объект сессии с БД..
        Defaults to fa.Depends(db.get_async_session).

    ### Yields:
        При обращении создаёт новое подключение к таблице `user` в БД.
    """
    yield SQLAlchemyUserDatabase(schemas.UserDB, session, models.UserTable)


def get_jwt_strategy() -> auth.JWTStrategy:
    """Получает настройки для использования `JWT`.

    ### Returns:
    - auth.JWTStrategy:
        Объект с настройками `JWT`.
    """
    return auth.JWTStrategy(
        secret=config.settings.secret,
        lifetime_seconds=const.JWT_LIFE_TIME
    )


bearer_transport = auth.BearerTransport(tokenUrl='auth/jwt/login')

auth_backend = auth.AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(fa_u.BaseUserManager[schemas.UserCreate, schemas.UserDB]):
    """Управление и проверки различных действий пользователя.

    ### Attrs:
    - user_db_model:
        Схема обрабатываемых данных.
    - reset_password_token_secret:
        Ключ для кодирования токена сброса пароля.
    - verification_token_secret:
        Ключ кодирования токена проверки.
    """
    user_db_model = schemas.UserDB
    reset_password_token_secret = config.settings.secret
    verification_token_secret = config.settings.secret

    async def validate_password(
        self,
        password: str,
        user: Union[schemas.UserCreate, schemas.UserDB],
    ) -> None:
        """Проверяет пароль пользователя.

        ### Args:
        - password (str):
            Введённый пароль.
        - user Union[schemas.UserCreate, schemas.UserDB]:
            Схема данных.

        ### Raises:
        - fa_u.InvalidPasswordException:
            Слишком короткий пароль.
       - fa_u.InvalidPasswordException:
            Пароль содержит e-mail пользователя.
        """
        if len(password) < 3:
            raise fa_u.InvalidPasswordException(
                reason=const.ERR_LEN_PASSWORD
            )
        if user.email in password:
            raise fa_u.InvalidPasswordException(
                reason=const.ERR_EMAIL_IN_PASSWORD
            )

    async def on_after_register(
            self,
            user: schemas.UserDB,
            request: Union[None, fa.Request] = None
    ):
        """Действия после регистрации пользователя.

        ### Args:
        - user (schemas.UserDB):
            Схема данных пользователя.
        - request (Union[None, fa.Request]):
            Объект запроса.
            Defaults to None.
        """
        print(const.USER_IS_SIGNED)


async def get_user_manager(user_db=fa.Depends(get_user_db)):
    """Генератор объектов `UserManager`.

    ### Args:
    - user_db (_type_, optional):
        Подключение к таблице `user` в БД.
        Defaults to fa.Depends(get_user_db).

    ### Yields:
        При обращении создаёт новый объект управления пользователями.
    """
    yield UserManager(user_db)

fastapi_users = fa_u.FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
    user_model=schemas.User,
    user_create_model=schemas.UserCreate,
    user_update_model=schemas.UserUpdate,
    user_db_model=schemas.UserDB
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
