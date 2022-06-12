"""Настройки для создания таблиц в БД и подключений к ней.
"""
from sqlalchemy import Column, Integer, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Подготовительный класс для ORM-моделей.

    Устанавливает для наследников название таблиц в формате `lowercase`
    и автоматическое добавление столбца `id` с типом `int`.

    ### Attrs:
    - id:
        Столбец для первичного ключа.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

async_engine = create_async_engine(
    settings.database_url,
    echo=settings.echo
)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    """Генератор объектов сессий подключения к БД.

    ### Returns:
    - AsyncSession:
        Объект сессии с БД.

    ### Yields:
        При обращении создаёт новый объект сессии с БД.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session

datetime_func = None
if settings.database_url.startswith('sqlite'):
    datetime_func = func.julianday
else:
    raise Exception(
        'Не определена функция извлечения времени из БД!'
    )
