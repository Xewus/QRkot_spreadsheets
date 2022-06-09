import os
import contextlib
from datetime import datetime

import uuid
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi_users import models
from fastapi_users.password import PasswordHelper
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user import UserCreate
from app.core.user import get_user_db, get_user_manager
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

try:
    from app.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
        'Проверьте и поправьте: они должны быть доступны в модуле `app.core.db`.',
    )

try:
    from app.core.user import current_superuser, current_user
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `current_superuser, current_user`.'
        'Проверьте и поправьте: они должны быть доступны в модуле `app.code.user`',
    )

try:
    from app.main import app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения `app`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `app.main`.',
    )

try:
    from app.core import google_client
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `google_client`. '
        'Проверьте и поправьте: он должн быть доступен в модуле `app.core`.',
    )

from app.core.google_client import get_service
from pathlib import Path

BASE_DIR = Path('.').absolute()
APP_DIR = BASE_DIR / 'app'


SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)


password_helper = PasswordHelper()
password_hash = password_helper.hash('chimichangas4life')

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


class User(models.BaseUser):
    pass


class UserDB(User, models.BaseUserDB):
    pass


user_uuid4 = uuid.uuid4()
user = UserDB(
    id=user_uuid4,
    email='dead@pool.com',
    hashed_password=str(password_hash),
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

superuser_uuid4 = uuid.uuid4()
superuser = UserDB(
    id=superuser_uuid4,
    email='superdead@pool.com',
    hashed_password=str(password_hash),
    is_active=True,
    is_verified=True,
    is_superuser=True,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    (BASE_DIR / 'test.db').absolute().unlink()


@pytest.fixture
def user_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def superuser(user_client):
    async with TestingSessionLocal() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(
                    UserCreate(
                        id=uuid.uuid4(),
                        email='superdead@pool.com',
                        password='chimichangas4life',
                        is_active=True,
                        is_verified=True,
                        is_superuser=True,
                    )
                )
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = user_client.post("/auth/jwt/login", data={"username": "superdead@pool.com", "password": 'chimichangas4life'}, headers=headers)
    return response.json()['access_token']


@pytest.fixture
async def simple_user(user_client):
    async with TestingSessionLocal() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(
                    UserCreate(
                        id=uuid.uuid4(),
                        email='dead@pool.com',
                        password='chimichangas4life',
                        is_active=True,
                        is_verified=True,
                        is_superuser=False,
                    )
                )
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = user_client.post("/auth/jwt/login", data={"username": "dead@pool.com", "password": 'chimichangas4life'}, headers=headers)
    return response.json()['access_token']


@pytest.fixture
def superuser_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_superuser] = lambda: superuser
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mixer():
    engine = create_engine('sqlite:///./test.db')
    session = sessionmaker(bind=engine)
    return _mixer(session=session(), commit=True)


@pytest.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def charity_project(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='chimichangas4life',
        user_email='dead@pool.com',
        description='Huge fan of chimichangas. Wanna buy a lot',
        full_amount=1000000,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def charity_project_nunchaku(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='nunchaku',
        user_email='evil@pool.com',
        description='Nunchaku is better',
        full_amount=5000000,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def small_fully_charity_project(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='1M$ for u project',
        user_email='elon@tusk.com',
        description='Wanna buy you project',
        full_amount=100,
        fully_invested=True,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        user_id=user_uuid4,
        full_amount=1000000,
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_email='evil@pool.com',
        invest_amount=100,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def dead_pool_donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        user_id=user_uuid4,
        full_amount=1000000,
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_email='dead@pool.com',
        invest_amount=100,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def small_donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_email='evil@pool.com',
        full_amount=50,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )
