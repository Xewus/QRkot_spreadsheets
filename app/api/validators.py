"""Функции проверок данных.
"""
from app import models, schemas
from app.core import db
from app.crud import charity_projects_crud as chr_crud
from app.services import constants as const
from app.services import exceptions as exc


async def project_name_is_busy(
    name: str,
    session: db.AsyncSession
) -> None:
    """Проверяет, свободно ли указанное название.

    ### Args:
    - name (str):
        Проверяемое назваие.
    - session (db.AsyncSession):
        Объект сессии с БД.

    ### Raises:
    - HTTPException:
        Указанное название уже занято.
    """
    if await chr_crud.get_by_field(
        required_field='name',
        value=name,
        session=session
    ):
        raise exc.HTTPExceptionBadRequest(
            detail=const.ERR_NAME_EXIST
        )


async def has_investition(
    project_id: int,
    session: db.AsyncSession
) -> models.CharityProject:
    """Проверяет, были ли уже инвестиции в указаный проект.

    ### Args:
    - project_id (int):
        `id` проверяемого благотворительного проекта.
    - session (db.AsyncSession):
        Объект сессии с БД.

    ### Raises:
    - HTTPException:
        Проект с указанным `id` не найден.
    - HTTPException:
        В указанный проект уже сделаны инвестиции.

    ### Returns:
    - models.CharityProject:
        Проверенный благотворительный проект.
    """
    project = await chr_crud.get(
        obj_id=project_id,
        session=session
    )
    if project is None:
        raise exc.HTTPExceptionBadRequest(
            detail=const.ERR_NOT_FOUND
        )
    if project.invested_amount > 0:
        raise exc.HTTPExceptionUnprocessableEntity(
            detail=const.ERR_HAS_INVEST % project.invested_amount
        )

    return project


async def allow_update_project(
    project_id: int,
    session: db.AsyncSession,
    update_data: schemas.CharityProjectUpdate
) -> models.CharityProject:
    """Проверяет, можно ли изменять указанный благотворительный проект.

    Проект должен быть открыт.
    Новая сумма требуемых инвестиций не может быть меньше уже имеющихся.

    ### Args:
    - update_data (Union[None, schemas.CharityProjectUpdate], optional):
        Обновляемые данные.
        Defaults to None.

    ### Raises:
    - HTTPException:
        Проект с указанным `id` не найден.
    - HTTPException:
        Проект уже закрыт.
    - HTTPException:
        Введённая сумма превышает уже инвестированную!

    ### Returns:
    - models.CharityProject:
        Проверенный благотворительный проект.
    """
    project = await chr_crud.get(
        obj_id=project_id,
        session=session
    )
    if project is None:
        raise exc.HTTPExceptionBadRequest(
            detail=const.ERR_NOT_FOUND
        )
    if project.fully_invested:
        raise exc.HTTPExceptionBadRequest(
            detail=const.ERR_PROJECT_CLOSED
        )
    if (
        update_data.full_amount and
        update_data.full_amount < project.invested_amount
    ):
        raise exc.HTTPExceptionBadRequest(
            detail=const.ERR_FULL_AMOUNT
        )
    if update_data.name and update_data.name != project.name:
        await project_name_is_busy(update_data.name, session)

    return project
