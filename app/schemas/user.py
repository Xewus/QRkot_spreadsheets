"""Схемы регламентирующие обмен данными для работы с моделью `UserTable`.
"""

from fastapi_users import models


class User(models.BaseUser):
    """схема с базовыми полями модели пользователя (за исключением пароля).
    """
    pass


class UserCreate(models.BaseUserCreate):
    """Схема для регистрации пользователя;

    Обязательно должны быть переданы email и password.
    Любые другие поля, передаваемые в запросе будут проигнорированы.
    """
    pass


class UserUpdate(models.BaseUserUpdate):
    """схема для обновления объекта пользователя.

    Содержит все базовые поля модели (в том числе и пароль).
    Все поля опциональны. Если запрос передаёт обычный пользователь
    (а не суперюзер), то поля is_active, is_superuser, is_verified исключаются.
    """
    pass


class UserDB(User, models.BaseUserDB):
    """схема, описывающая модель в БД.
    """
    pass
