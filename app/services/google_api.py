"""Функции взаимодействия приложения с Google API.
"""
from datetime import timedelta
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject
from app.services import constants as const


async def spreadsheet_create(wrapper_service: Aiogoogle) -> str:
    """Создаёт таблицу.
    ### Args:
    - wrapper_service (Aiogoogle):
        ...
    ### Returns:
    - str:
        `id` созданной таблицы.
    """
    service = await wrapper_service.discover(
        api_name='sheets',
        api_version='v4'
    )
    spreadsheet_body = {
        'properties': {
            'title': const.TABLE_NAME,
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': const.SHEET_NAME_RATING_SPEED_CLOSING,
                'gridProperties': {
                    'rowCount': 50,
                    'columnCount': 5
                }
            }}
        ]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    """Получает разрешение на доступ к таблице.
    ### Args:
    - spreadsheet_id (str):
        `id` таблицы.
    - wrapper_service (Aiogoogle):
        ...
    """
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover(
        api_name='drive',
        api_version='v3'
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def get_spreadsheet_id(wrapper_service: Aiogoogle) -> str:
    """Получает `id` таблицы. Если таковой не существует - создаёт новую.

    ### Args:
    - wrapper_service (Aiogoogle):
        ...

    ### Returns:
    - str:
        `id` таблицы.
    """
    service = await wrapper_service.discover(
        api_name='drive',
        api_version='v3'
    )
    response = await wrapper_service.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )

    spreadsheet_id = None
    table = response['files']

    if len(table) > 0:
        for spreadsheet in table:
            if spreadsheet['name'] == const.TABLE_NAME:
                spreadsheet_id = spreadsheet['id']
                break

    if spreadsheet_id is None:
        spreadsheet_id = spreadsheet_create(
            wrapper_service=wrapper_service
        )
    return spreadsheet_id


async def spreadsheet_update_value(
    spreadsheet_id: str,
    projects: List[CharityProject],
    wrapper_service: Aiogoogle
) -> None:
    """Обновляет данные таблицы.

    ### Args:
    - spreadsheet_id (str):
        Обновляемая таблица.
    - projects (List[CharityProject]):
        Список данных для обновления.
    - wrapper_service (Aiogoogle):
        ...
    """
    service = await wrapper_service.discover(
        api_name='sheets',
        api_version='v4'
    )
    await set_user_permissions(
        spreadsheet_id=spreadsheet_id,
        wrapper_service=wrapper_service
    )
    table_values = [[
        'Название проекта',
        'Время, затраченное на сбор средств',
        'Описание'
    ]]
    for project in projects:
        table_values.append([
            project.name,
            str(timedelta(project.lifetime)),
            project.description
        ])
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
