"""Эндпоинты для обработки обращений к `Google API`.
"""
from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app import schemas
from app.core import db, user
from app.core.google_client import get_service
from app.crud import charity_projects_crud as chr_crud
from app.services import constants as const
from app.services import google_api as go_service
from app.services import utils

router = APIRouter()


@router.get(
    path='/',
    summary=const.GET_REPORT_TO_GOOGLE,
    response_model=schemas.GoogleAPIStringResponseSchema,
    dependencies=[Depends(user.current_superuser)]
)
async def get_report(
    session: db.AsyncSession = Depends(db.get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> Dict[str, str]:
    """Отпраляет отчёт по скорости закрытия проектов в `googlesheets`.

    ### Args:
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).
    - wrapper_service (Aiogoogle, optional):
        Ассихронный сервис работы с Google.
        Defaults to Depends(get_service).

    ### Returns:
    - Dict:
        Ссылка на таблицу с данными.
    """
    closed_projects = await chr_crud.get_by_field(
        required_field='fully_invested',
        value=True,
        session=session,
        one_obj=False
    )
    closed_projects.sort(key=utils.sort_by_timdelta)

    spreadsheet_id = await go_service.get_exist_id(
        wrapper_service=wrapper_service
    )

    if spreadsheet_id is None:
        spreadsheet_id = await go_service.spreadsheet_create(
            wrapper_service=wrapper_service
        )

    await go_service.set_user_permissions(
        spreadsheet_id=spreadsheet_id,
        wrapper_service=wrapper_service
    )
    await go_service.spreadsheet_update_value(
        spreadsheet_id=spreadsheet_id,
        projects=closed_projects,
        wrapper_service=wrapper_service
    )
    return {'url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'}
