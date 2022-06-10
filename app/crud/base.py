"""Сборник базовых операций CRUD.
"""
from typing import Any, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, select

from app import schemas
from app.core import db
from app.services import constants as const
from app.services import utils

ModelType = TypeVar('ModelType', bound=db.Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=schemas.BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=schemas.BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс с операциями CRUD.
    """
    def __init__(
        self,
        model: Type[ModelType]
    ) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: db.AsyncSession
    ) -> Union[None, ModelType]:
        """Получает объект из БД по `id`.

        ### Args:
        - obj_id (int):
            `id` искомого объекта.
        - session (db.AsyncSession):
            Объект сессиис БД.

        ### Returns:
        - None | ModelType:
            Найденный объект.
        """
        return await session.get(self.model, obj_id)

    async def get_all(
        self,
        session: db.AsyncSession
    ) -> List[ModelType]:
        """Получает все объекты из запрошенной таблицы.

        ### Args:
        - session (db.AsyncSession):
            Объект сессии с БД.

        ### Returns:
        - list[ModelType]:
            Список объектов.
        """
        objects = await session.scalars(
            select(self.model)
        )
        return objects.all()

    async def get_by_field(
        self,
        required_field: str,
        value: Any,
        session: db.AsyncSession,
        one_obj: bool = True
    ) -> Union[ModelType, List[ModelType]]:
        """Находит объекты по значению указанного поля.

        ### Args:
        - field (str):
            Поле, по которому ведётся поиск.
        - value (Any):
            Искомое значение.
        - session (db.AsyncSession):
            Объект сессии с БД.
        - one_obj (bool, optional):
            Вернуть один или все найденные объекты.
            Defaults to True.
        - order_by (Union[None, str]):
            По какому полю упорядочить запрос.
            Defaults to None.

        ### Raises:
        - AttributeError:
            Указанное поле отсутствует в таблице.

        ### Returns:
        - Union[ModelType, List[ModelType]]:
            Найденные объекты.
        """
        field = getattr(self.model, required_field, None)
        if field is None:
            raise AttributeError(
                const.ERR_NO_TABLE_FIELD % required_field
            )

        query = select(self.model).where(field == value)

        if one_obj:
            return await session.scalar(query.limit(1))

        some_objs = await session.scalars(query)

        return some_objs.all()

    async def get_for_distribution(
        self,
        session: db.AsyncSession
    ) -> Union[ModelType, List[ModelType]]:
        """Получает все объекты с незакрытыми инвестициями.

        ### Args:
        - session (db.AsyncSession):
            Объект сесси с БД.

        ### Returns:
        - Union[ModelType, List[ModelType]]:
            Найденные объекты.
        """
        objs = await session.scalars(
            select(
                self.model
            ).where(
                self.model.fully_invested.is_(False)
            ).order_by(
                asc('create_date')
            )
        )
        return objs.all()

    async def create(
        self,
        new_obj: CreateSchemaType,
        session: db.AsyncSession,
        user: Union[None, schemas.UserDB] = None
    ) -> ModelType:
        """Создаёт запись в БД.

        ### Args:
        - data (CreateSchemaType):
            Данные для записи в БД.
        - session (db.AsyncSession):
            Объект сессии.
        - user (None | schemas.UserDB, optional):
            Пользователь, создавший с запись.
            Defaults to None.

        ### Returns:
        - ModelType: Объект, записаный в БД.
        """
        new_obj = new_obj.dict()

        if user is not None:
            new_obj['user_id'] = user.id

        new_obj = self.model(**new_obj)
        session.add(new_obj)
        return await utils.try_commit_to_db(
            obj=new_obj,
            session=session
        )

    async def update(
        self,
        obj: ModelType,
        session: db.AsyncSession,
        update_data: UpdateSchemaType,
    ) -> ModelType:
        """Обновляет запись указанного объекта в БД.

        ### Args:
        - obj (ModelType):
            Редактируемый объект.
        - session (db.AsyncSession):
            Объект сессии с БД.
        - update_data (UpdateSchemaType):
            Обновляемые данные.

        ### Returns:
        - ModelType:
            Обновлённый объект.
        """
        obj_data = jsonable_encoder(obj)

        update_data = update_data.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])

        return await utils.try_commit_to_db(
            obj=obj,
            session=session
        )

    async def remove(
        self,
        obj: db.Base,
        session: db.AsyncSession
    ) -> ModelType:
        """Удаляет запись из БД.

        ### Args:
        - obj (db.Base):
            Удаляемый объект.
        - session (db.AsyncSession):
            Объект сессии.

        ### Returns:
        - ModelType:
            Удалённый объект.
            Данные объекта всё ещё хранятся в сессии после удаления из БД.
        """
        await session.delete(obj)
        await session.commit()
        return obj
