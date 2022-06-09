"""Различные вспомогательные функции.
"""
from datetime import datetime

from app.core import db
from app.services import exceptions as exc
from app.services import constants as const


async def try_commit_to_db(
    obj: db.Base,
    session: db.AsyncSession
) -> db.Base:
    """Пытается записать данные в БД с обработкой ошибок.

    ### Args:
    - obj (db.Base):
        Объект для записи в БД.
    - session (db.AsyncSession):
        Объект сессий с БД.

    ### Raises:
    - exc.HTTPExceptionInternalServerError:
        Записываемые данные не консистентны.
    - exc.HTTPExceptionInternalServerError:
        Иные ошибки при соединении с БД.

    ### Returns:
    - db.Base:
        Записаный а БД объект.
    """
    try:
        await session.commit()
        await session.refresh(obj)
        return obj
    except exc.IntegrityError:
        raise exc.HTTPExceptionInternalServerError(
            detail=const.ERR_BASE_INTEGRITY
        )
    except Exception:
        raise exc.HTTPExceptionInternalServerError(
            detail=const.ERR_BASE_ANY
        )


def close_obj(obj: db.Base) -> None:
    """Закрывает объекты с рапределёнными инвестициями.

    ### Args:
    - obj (db.Base):
        Проверяемый объект.
    """
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.now()


async def distribution_of_amounts(
    undivided: db.Base,
    crud_class: db.Base,
    session: db.AsyncSession
) -> None:
    """Разделяет доступную сумму переданного объекта
    по доступным местам в другие объекты.

    Все объекты должны иметь поля -
    `full_amount`, `invested_amount`, `fully_invested`, `created_date`.

    ### Args:
    - undivided (CRUDBase):
        Объект, содержащий поле `full_amount`
        из которого будет производится распределение.
    - crud_class (CRUDBase):
        Класс, имеющий метод `get_by_field`, возвращающий объекты,
        в которые возможно распределить сумму.
    - session (db.AsyncSession):
        Объект сессии с БД.
    """
    receptions = await crud_class.get_for_distribution(
        session=session
    )
    for reception in receptions:
        needed = undivided.full_amount - undivided.invested_amount
        if not needed:
            break
        available = reception.full_amount - reception.invested_amount
        to_add = min(needed, available)
        reception.invested_amount += to_add
        undivided.invested_amount += to_add
        close_obj(reception)

    close_obj(undivided)

    await try_commit_to_db(
        obj=undivided,
        session=session
    )


def normalize_datetime(values: dict) -> dict:
    """Изменяет строковый формат даты в формат `ISO`.

    ### Args:
    - values (dict):
        Словарь с датами.

    ### Returns:
    - dict:
        Словарь с отформатированными датами.
    """
    for date in ('create_date', 'close_date'):
        if values.get(date) is not None:
            values[date] = values[date].isoformat(
                timespec=const.TIMESPEC
            )
    return values


def sort_by_timdelta(obj):
    return obj.close_date - obj.create_date