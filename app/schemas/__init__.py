"""Модуль со схемами, регламентирущими входные и выходные данные.
"""
from .charity_project import (BaseModel, CharityProjectCreate,  # noqa
                              CharityProjectResponse, CharityProjectUpdate)
from .donation import (DonationCreate, DonationLongResponse,  # noqa
                       DonationShortResponse)
from .google_api import GoogleAPIBaseSchema  # noqa
from .google_api import GoogleAPIStringResponseSchema
from .user import User, UserCreate, UserDB, UserUpdate  # noqa
