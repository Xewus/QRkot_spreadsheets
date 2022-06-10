"""Модуль со схемами, регламентирущими входные и выходные данные.
"""
from .charity_project import (  # noqa
    BaseModel,
    CharityProjectCreate,
    CharityProjectResponse,
    CharityProjectUpdate
)
from .google_api import(        # noqa
    GoogleAPIBaseSchema,
    GoogleAPIStringResponseSchema
)
from .donation import (         # noqa
    DonationCreate,
    DonationLongResponse,
    DonationShortResponse
)
from .user import (             # noqa
    User,
    UserCreate,
    UserDB,
    UserUpdate
)
