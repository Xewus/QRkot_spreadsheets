import pytest


@pytest.mark.parametrize('json, keys, expected_data', [
    (
        {'full_amount': 10},
        ['full_amount', 'id', 'create_date'],
        {'full_amount': 10, 'id': 1},
    ),
    (
        {'full_amount': 5, 'comment': 'To you for chimichangas'},
        ['full_amount', 'id', 'create_date', 'comment'],
        {'full_amount': 5, 'id': 1, 'comment': 'To you for chimichangas'},
    ),
])
def test_create_donation(user_client, json, keys, expected_data):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 200, (
        'При создании пожертвования должен возвращаться статус-код 200.'
    )
    data = response.json()
    assert sorted(list(data.keys())) == sorted(keys), (
        f'При создании пожертвования в ответе должны быть ключи `{keys}`.'
    )
    data.pop('create_date')
    assert data == expected_data, (
        'При создании пожертвования тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'comment': 'To you for chimichangas'},
    {'full_amount': -1},
    {'full_amount': None},
])
def test_create_donation_incorrect(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'При некорректном теле POST-запроса к эндпоинту `/donation/` '
        'должен вернуться статус-код 422.'
    )


def test_get_user_donation(user_client, dead_pool_donation):
    response = user_client.get('/donation/my')
    assert response.status_code == 200, (
        'При получении списка пожертвований пользователя должен вернуться статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При получении списка пожертвований пользователя должен возвращаться объект типа `list`.'
    )
    assert len(response.json()) == 1, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не создаётся объект в БД.'
        'Проверьте модель `Donation`.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении списка пожертвований пользователя в ответе должны быть ключи `{keys}`.'
    )
    assert response.json() == [{
        'comment': 'To you for chimichangas',
        'create_date': '2019-09-24T14:15:22',
        'full_amount': 1000000,
        'id': 1,
    }], 'При получении списка пожертвований пользователя тело ответа API отличается от ожидаемого.'


def test_get_all_donations(superuser_client, donation):
    response = superuser_client.get('/donation/')
    assert response.status_code == 200, (
        'При получении списка всех пожертвований должен возвращаться статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При получении списка всех пожертвований  должен возвращаться объект типа `list`.'
    )
    assert len(response.json()) == 1, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не создаётся объект в БД. '
        'Проверьте модель `Donation`.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении списка всех пожертвований в ответе должны быть ключи `{keys}`.'
    )
    data = response.json()
    data[0].pop('user_id')
    assert data == [{
        'close_date': '2019-08-24T14:15:22',
        'comment': 'To you for chimichangas',
        'create_date': '2019-09-24T14:15:22',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
    }], 'При получении списка всех пожертвований тело ответа API отличается от ожидаемого.'
