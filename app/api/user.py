"""Эндпоинты для обработки обращений к `User`.
"""
from fastapi import APIRouter
from pydantic import UUID4

from app.core import user
from app.services import constants as const
from app.services import exceptions as exc

router = APIRouter()

router.include_router(
    router=user.fastapi_users.get_auth_router(user.auth_backend),
    prefix='/auth/jwt',
    tags=['Auth']
)
router.include_router(
    user.fastapi_users.get_register_router(),
    prefix='/auth',
    tags=['Auth'],
)
router.include_router(
    user.fastapi_users.get_users_router(),
    prefix='/users',
    tags=['Users'],
)


@router.delete(
    '/users/{id}',
    tags=['Users'],
    deprecated=True
)
def delete_user(id: UUID4) -> None:
    """Не используйте удаление, деактивируйте пользователей.
    """
    raise exc.HTTPExceptionMethodNotAllowed(
        detail=const.ERR_NO_DELETE_USER
    )
