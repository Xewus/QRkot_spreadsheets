"""Эндпоинты для обработки обращений к `Donation`.
"""
from typing import List

from fastapi import APIRouter, Depends

from app import schemas
from app.core import db, user
from app.crud import charity_projects_crud as ch_pr_crud
from app.crud import donation_crud as dn_crud
from app.services import constants as const
from app.services import utils

router = APIRouter()


@router.get(
    path='/',
    summary=const.GET_ALL_DONATIONS,
    response_model=List[schemas.DonationLongResponse],
    dependencies=[Depends(user.current_superuser)]
)
async def get_all_donations(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[schemas.DonationLongResponse]:
    """Получает список всех пожертвований.

    Только для суперюзеров.

    ### Args:
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - List[schemas.DonationListResponse]:
        Список всех пожертвований.
    """
    return await dn_crud.get_all(session=session)


@router.post(
    path='/',
    summary=const.CREATE_DONATION,
    response_model=schemas.DonationShortResponse,
    response_model_exclude_none=True
)
async def create_donation(
    new_donation: schemas.DonationCreate,
    session: db.AsyncSession = Depends(db.get_async_session),
    user: schemas.UserDB = Depends(user.current_user)
) -> schemas.DonationShortResponse:
    """Записывает новое пожертвование.

    ### Args:
    - new_donation (schemas.DonationCreate):
        Данные для записи нового пожертвования.
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).
    - user (schemas.UserDB, optional):
        Данные пользователя, сделавшего пожертвование.
        Defaults to Depends(user.current_user).

    ### Returns:
    - schemas.DonationShortResponse:
        Новое учтённое пожертвование.
    """
    donation = await dn_crud.create(
        new_obj=new_donation,
        session=session,
        user=user
    )
    await utils.distribution_of_amounts(
        undivided=donation,
        crud_class=ch_pr_crud,
        session=session
    )

    return donation


@router.get(
    path='/my',
    summary=const.GET_MY_DONATIONS,
    response_model=List[schemas.DonationShortResponse]
)
async def get_user_donations(
    user: schemas.UserDB = Depends(user.current_user),
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[schemas.DonationShortResponse]:
    """Получает список пожертвований пользователя.

    ### Args:
    - user (schemas.UserDB, optional):
        Данные запрашивающего пользоваиеля.
        Defaults to Depends(user.current_user).
    - session (db.AsyncSession, optional):
        Объект сессии с БД.
        Defaults to Depends(db.get_async_session).

    ### Returns:
    - List[schemas.DonationShortResponse]:
        Список всех пожертвований пользователя.
    """
    return await dn_crud.get_my_donations(
        user_id=user.id,
        session=session
    )
