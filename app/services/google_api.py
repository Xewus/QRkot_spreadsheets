"""Функции взаимодействия приложения с Google API.
"""
from typing import List, Union

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services import constants as const
from app.models import CharityProject


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


async def get_exist_id(wrapper_service: Aiogoogle) -> Union[None, str]:
    """Получает `id` таблицы, если таковая существует.

    ### Args:
    - wrapper_service (Aiogoogle):
        _description_

    ### Returns:
    - str:
        _description_
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
    table = response['files']
    if len(table) == 0:
        return None
    for sheet in table:
        if sheet['name'] == const.TABLE_NAME:
            return sheet['id']


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
    table_values = [[
        'Название проекта',
        'Время, затраченное на сбор средств',
        'Описание'
    ]]
    for project in projects:
        delta = project.create_date - project.close_date
        table_values.append([
            project.name,
            delta.seconds,
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
