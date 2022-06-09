"""Эндпоинты для обработки обращений к `CharityProject`.
"""
from typing import List

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from app import schemas
from app.api import validators
from app.core import db, user
from app.crud import charity_projects_crud as ch_pr_crud
from app.crud import donation_crud as dn_crud
from app.services import constants as const
from app.services import utils

router = APIRouter()


@router.get(
    path='/',
    summary=const.GET_ALL_CHARITY_PROJECTS,
    response_model=List[schemas.CharityProjectResponse]
)
async def get_all_charity_projects(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[schemas.CharityProjectResponse]:
    """Получает список всех благотварительных проектов.

    ### Args:
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - List[schemas.CharityProjectResponse]:
        Список всех благотварительных проектов.
    """
    return await ch_pr_crud.get_all(
        session=session
    )


@router.post(
    path='/',
    summary=const.CREATE_CHARITY_PROJECTS,
    response_model=schemas.CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def create_charity_project(
    new_project: schemas.CharityProjectCreate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """Создает новый благотворительный проект.

    Только для суперюзеров.

    ### Args:
    - new_project (Cschemas.harityProjectCreateS:
        Данные для создания нового благотворительного проекта.
    - session (db.AsyncSession, optional):
        Объект сесси с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - schemas.CharityProjectResponse:
        Вновь созданный благотворителный проект.
    """
    await validators.project_name_is_busy(
        name=new_project.name,
        session=session
    )
    project = await ch_pr_crud.create(
        new_obj=new_project,
        session=session
    )
    await utils.distribution_of_amounts(
        undivided=project,
        crud_class=dn_crud,
        session=session
    )

    return project


@router.patch(
    path='/{project_id}',
    summary=const.UPDATE_CHARITY_PROJECT,
    response_model=schemas.CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def update_charity_project(
    project_id: PositiveInt,
    update_data: schemas.CharityProjectUpdate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """Обновляет сущствующий благотворительный проект.

    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    Только для суперюзеров.

    ### Args:
    - project_id (int):
       `id` редактируемого благотворительного проекта.
    - update_data (schemas.CharityProjectUpdate):
        Данные для обновления.
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - schemas.CharityProjectResponse:
        Обновлённый благотворительный проект.
    """
    project = await validators.allow_update_project(
        project_id=project_id,
        session=session,
        update_data=update_data
    )

    project = await ch_pr_crud.update(
        obj=project,
        session=session,
        update_data=update_data
    )
    await utils.distribution_of_amounts(
        undivided=project,
        crud_class=dn_crud,
        session=session
    )
    return project


@router.delete(
    path='/{project_id}',
    summary=const.DELETE_CHARITY_PROJECTS,
    response_model=schemas.CharityProjectResponse,
    dependencies=[Depends(user.current_superuser)]
)
async def delete_charity_project(
    project_id: PositiveInt,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """Удаляет благотворительный проект.

    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    Только для суперюзеров.

    ### Args:
    - project_id (int):
        `id`удаляемого благотворительно проекта.
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - schemas.CharityProjectResponse:
        Удалённый благотворительный проект.
    """
    project = await validators.has_investition(
        project_id=project_id,
        session=session
    )

    return await ch_pr_crud.remove(
        obj=project,
        session=session
    )
