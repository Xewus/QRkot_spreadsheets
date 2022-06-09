
def test_donation_move_second_project_first_full(
        user_client,
        charity_project,
        charity_project_nunchaku,
):
    response = user_client.post('/donation/', json={
        'full_amount': 1000001,
        'comment': 'From Elon Tusk',
    })
    response = user_client.get('/charity_project/')
    data = response.json()

    def del_date(record: dict):
        try:
            del record['close_date']
            del record['create_date']
        except KeyError:
            raise AssertionError(
                'При получении всех проектов в ответе отсутствуют '
                'ключи `close_date` и `create_date`.',
            )
        return record
    data = list(map(del_date, data))
    assert data == [
        {
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': True,
            'id': 1,
            'invested_amount': 1000000,
            'name': 'chimichangas4life',
        },
        {
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 1,
            'name': 'nunchaku',
        },
    ]


def test_donation_create_project_doesnt_exists(superuser_client, donation):
    response_donation = superuser_client.get('/donation/')
    data_donation = response_donation.json()
    assert len(data_donation) == 1, (
        'Если получено пожертвование, но открытых проектов нет, '
        'вся сумма из пожертвования должна ожидать открытия нового проекта.'
    )
    superuser_client.post('/charity_project/', json={
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'full_amount': 1000000,
    })
    response_project = superuser_client.get('/charity_project/')
    data_project = response_project.json()
    assert len(data_project) == 1, (
        'Если открытых проектов нет - '
        'все свободные деньги должны ожидать открытия нового проекта. '
        'При создании нового проекта свободные инвестиции должны быть направлены на этот проект.'
    )
