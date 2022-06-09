from app.models import CharityProject, Donation
from sqlalchemy.future import select
import pytest


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        "lovechimichangasbutnunchakuisbetternunchakis4life" * 3,
    ],
)
def test_create_invalid_project_name(superuser, test_client, invalid_name):
    headers = {"Authorization": f"Bearer {superuser}"}

    response = test_client.post(
        "/charity_project/",
        json={
            "name": invalid_name,
            "description": "Project_1",
            "full_amount": 5000,
        },
        headers=headers,
    )

    assert (
        response.status_code == 422
    ), "Нельзя создать проект с пустым названием или с названием длиннее 100 символов."


@pytest.mark.parametrize(
    "invalid_full_amount",
    [
        -100,
        0.5,
        "test",
        0.0,
    ],
)
def test_create_invalid_full_amount_value(superuser, test_client, invalid_full_amount):
    headers = {"Authorization": f"Bearer {superuser}"}

    response = test_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": invalid_full_amount,
        },
        headers=headers,
    )

    assert (
        response.status_code == 422
    ), "Требуемая сумма (full_amount) проекта должна быть целочисленной и больше 0."


def test_get_charity_project(user_client, charity_project):
    response = user_client.get("/charity_project/")
    assert (
        response.status_code == 200
    ), "При GET-запросе к эндпоинту `/charity_project/` должен возвращаться статус-код 200."
    assert isinstance(
        response.json(), list
    ), "При GET-запросе к эндпоинту `/charity_project/` должен возвращаться объект типа `list`."
    assert len(response.json()) == 1, (
        "При корректном POST-запросе к эндпоинту `/charity_project/` не создаётся объект в БД. "
        "Проверьте модель `CharityProject`."
    )
    data = response.json()[0]
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"При GET-запросе к эндпоинту `/charity_project/` в ответе API должны быть ключи `{keys}`."
    assert response.json() == [
        {
            "close_date": "2019-08-24T14:15:22",
            "create_date": "2019-08-24T14:15:22",
            "description": "Huge fan of chimichangas. Wanna buy a lot",
            "full_amount": 1000000,
            "fully_invested": False,
            "id": 1,
            "invested_amount": 0,
            "name": "chimichangas4life",
        }
    ], "При GET-запросе к эндпоинту `/charity_project/` тело ответа API отличается от ожидаемого."


def test_get_all_charity_project(
    user_client, charity_project, charity_project_nunchaku
):
    response = user_client.get("/charity_project/")
    assert (
        response.status_code == 200
    ), "При запросе всех проектов должен возвращаться статус-код 200."
    assert isinstance(
        response.json(), list
    ), "При запросе всех проектов должен возвращаться объект типа `list`."
    assert len(response.json()) == 2, (
        "При корректном POST-запросе к эндпоинту `/charity_project/` не создаётся объект в БД."
        "Проверьте модель `CharityProject`."
    )
    data = response.json()[0]
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"При запросе всех проектов в ответе API должны быть ключи `{keys}`."
    assert response.json() == [
        {
            "close_date": "2019-08-24T14:15:22",
            "create_date": "2019-08-24T14:15:22",
            "description": "Huge fan of chimichangas. Wanna buy a lot",
            "full_amount": 1000000,
            "fully_invested": False,
            "id": 1,
            "invested_amount": 0,
            "name": "chimichangas4life",
        },
        {
            "close_date": "2019-08-24T14:15:22",
            "create_date": "2019-08-24T14:15:22",
            "description": "Nunchaku is better",
            "full_amount": 5000000,
            "fully_invested": False,
            "id": 2,
            "invested_amount": 0,
            "name": "nunchaku",
        },
    ], "При запросе всех проектов тело ответа API отличается от ожидаемого."


def test_create_charity_project(superuser_client):
    response = superuser_client.post(
        "/charity_project/",
        json={
            "name": "Мертвый Бассейн",
            "description": "Deadpool inside",
            "full_amount": 1000000,
        },
    )
    assert (
        response.status_code == 200
    ), "При создании проекта должен возвращаться статус-код 200."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "create_date",
            "fully_invested",
            "id",
            "invested_amount",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"При создании проекта в ответе API должны быть ключи `{keys}`."
    data.pop("create_date")
    assert data == {
        "description": "Deadpool inside",
        "full_amount": 1000000,
        "fully_invested": False,
        "id": 1,
        "invested_amount": 0,
        "name": "Мертвый Бассейн",
    }, "При создании проекта тело ответа API отличается от ожидаемого."


@pytest.mark.parametrize(
    "json",
    [
        {
            "name": "Мертвый Бассейн",
            "full_amount": "1000000",
        },
        {
            "description": "Deadpool inside",
            "full_amount": "1000000",
        },
        {
            "name": "Мертвый Бассейн",
            "description": "Deadpool inside",
        },
        {
            "name": "Мертвый Бассейн",
            "description": "Deadpool inside",
            "full_amount": "Donat",
        },
        {
            "name": "Мертвый Бассейн",
            "description": "Deadpool inside",
            "full_amount": "",
        },
        {},
    ],
)
def test_create_charity_project_validation_error(json, superuser_client):
    response = superuser_client.post("/charity_project/", json=json)
    assert response.status_code == 422, (
        "При некорректном создании проекта должен возвращаться статус-код 422."
    )
    data = response.json()
    assert (
        "detail" in data.keys()
    ), "При некорректном создании проекта в ответе API должен быть ключ `detail`."


def test_delete_project_non_superuser(test_client, simple_user, superuser):
    headers = {"Authorization": f"Bearer {superuser}"}

    test_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": 5000,
        },
        headers=headers,
    )

    response = test_client.delete(
        "/charity_project/1", headers={"Authorization": f"Bearer {simple_user}"}
    )

    assert response.status_code == 403, "Только суперпользователь может удалить проект."


def test_delete_charity_project(superuser_client, charity_project):
    response = superuser_client.delete(f"/charity_project/{charity_project.id}")
    assert (
        response.status_code == 200
    ), "При удалении проекта должен возвращаться статус-код 200."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"При удалении проекта в ответе API должны быть ключи `{keys}`."
    assert data == {
        "name": "chimichangas4life",
        "description": "Huge fan of chimichangas. Wanna buy a lot",
        "full_amount": 1000000,
        "id": 1,
        "invested_amount": 0,
        "fully_invested": False,
        "create_date": "2019-08-24T14:15:22",
        "close_date": "2019-08-24T14:15:22",
    }, "При удалении проекта тело ответа API отличается от ожидаемого."


def test_delete_charity_project_invalid_id(superuser_client):
    response = superuser_client.delete("/charity_project/999a4")
    assert (
        response.status_code == 422
    ), "При некорректном удалении проекта должен возвращаться статус-код 422."
    data = response.json()
    assert (
        "detail" in data.keys()
    ), "При некорректном удалении проекта в ответе API должен быть ключ `detail`"


@pytest.mark.parametrize(
    "json, expected_data",
    [
        (
            {"full_amount": 10},
            {
                "name": "chimichangas4life",
                "description": "Huge fan of chimichangas. Wanna buy a lot",
                "full_amount": 10,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "create_date": "2019-08-24T14:15:22",
                "close_date": "2019-08-24T14:15:22",
            },
        ),
        (
            {"name": "chimi"},
            {
                "name": "chimi",
                "description": "Huge fan of chimichangas. Wanna buy a lot",
                "full_amount": 1000000,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "create_date": "2019-08-24T14:15:22",
                "close_date": "2019-08-24T14:15:22",
            },
        ),
        (
            {"description": "Give me the money!"},
            {
                "name": "chimichangas4life",
                "description": "Give me the money!",
                "full_amount": 1000000,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "create_date": "2019-08-24T14:15:22",
                "close_date": "2019-08-24T14:15:22",
            },
        ),
    ],
)
def test_update_charity_project(superuser_client, charity_project, json, expected_data):
    response = superuser_client.patch("/charity_project/1", json=json)
    assert (
        response.status_code == 200
    ), "При обновлении проекта должен возвращаться статус-код 200."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"При обновлении проекта в ответе API должны быть ключи `{keys}`."
    assert (
        data == expected_data
    ), "При обновлении проекта тело ответа API отличается от ожидаемого."


@pytest.mark.parametrize(
    "json",
    [
        {"desctiption": ""},
        {"name": ""},
        {"full_amount": ""},
    ],
)
def test_update_charity_project_invalid(superuser_client, charity_project, json):
    response = superuser_client.patch("/charity_project/1", json=json)
    assert response.status_code == 422, (
        "При некорректном обновлении проекта должен возвращаться статус-код 422."
    )


def test_create_charity_project_usual_user(user_client):
    response = user_client.post(
        "/charity_project/",
        json={
            "name": "Мертвый Бассейн",
            "description": "Deadpool inside",
            "full_amount": 1000000,
        },
    )
    assert (
        response.status_code == 401
    ), "При создании проекта не суперпользователем должен возвращаться статус-код 401."
    data = response.json()
    assert (
        "detail" in data
    ), "При создании проекта не суперпользователем в ответе API должен быть ключ `detail`."
    assert data == {
        "detail": "Unauthorized",
    }, "При создании проекта не суперпользователем тело ответа API отличается от ожидаемого."


def test_patch_charity_project_usual_user(user_client):
    response = user_client.patch("/charity_project/1", json={"full_amount": 10})
    assert (
        response.status_code == 401
    ), "При обновлении проекта не суперпользователем должен возвращаться статус-код 401."
    data = response.json()
    assert (
        "detail" in data
    ), "При обновлении проекта не суперпользователем в ответе должен быть ключ `detail`."
    assert data == {
        "detail": "Unauthorized",
    }, "При обновлении проекта не суперпользователем тело ответа API отличается от ожидаемого."


def test_patch_charity_project_fully_invested(
    superuser_client, small_fully_charity_project
):
    response = superuser_client.patch("/charity_project/1", json={"full_amount": 10})
    assert response.status_code == 400, (
        "При обновлении проекта, который был полностью проинвестирован, "
        "должен возвращаться статус-код 400."
    )
    data = response.json()
    assert "detail" in data, (
        "При обновлении проекта, который был полностью проинвестирован, "
        "в ответе должен быть ключ `detail`."
    )
    assert data == {"detail": "Закрытый проект нельзя редактировать!", }, (
        "При обновлении проекта, который был полностью "
        "проинвестирован, тело ответа API отличается от ожидаемого."
    )


def test_create_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.post(
        "/charity_project/",
        json={
            "name": "chimichangas4life",
            "description": "Huge fan of chimichangas. Wanna buy a lot",
            "full_amount": 1000000,
        },
    )
    assert response.status_code == 400, (
        "При создании проекта с неуникальным именем "
        "должен возвращаться статус-код 400."
    )
    data = response.json()
    assert "detail" in data, (
        "При создании проекта с неуникальным именем "
        "в ответе должен быть ключ `detail`."
    )
    assert data == {"detail": "Проект с таким именем уже существует!", }, (
        "При создании проекта с неуникальным именем "
        "тело ответа API отличается от ожидаемого."
    )


async def test_projects_should_be_closed_after_donation(
    superuser, user_client, session
):
    headers = {"Authorization": f"Bearer {superuser}"}
    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": 100,
        },
        headers=headers,
    )

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_2",
            "description": "Project_2",
            "full_amount": 100,
        },
        headers=headers,
    )

    user_client.post("/donation/", json={"full_amount": 50, "comment": "donation_1"})

    user_client.post("/donation/", json={"full_amount": 50, "comment": "donation_2"})

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 1)
    )
    charity_project_closed = result.scalars().first()
    await session.refresh(charity_project_closed)

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 2)
    )
    charity_project_open = result.scalars().first()
    await session.refresh(charity_project_open)

    assert (
        charity_project_closed.fully_invested is True
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )
    assert (
        charity_project_open.fully_invested is False
    ), "Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."


async def test_all_projects_fully_invested(superuser, user_client, session):
    headers = {"Authorization": f"Bearer {superuser}"}

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": 100,
        },
        headers=headers,
    )

    user_client.post("/donation/", json={"full_amount": 200, "comment": "donation_1"})

    user_client.post("/donation/", json={"full_amount": 200, "comment": "donation_2"})

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 1)
    )

    first_charity_project_closed = result.scalars().first()

    result = await session.execute(select(Donation).filter(Donation.id == 1))

    first_donation_amount = result.scalars().first()

    assert (
        first_charity_project_closed.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert (
        first_donation_amount.invested_amount == 100
    ), f"Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_2",
            "description": "Project_2",
            "full_amount": 150,
        },
        headers=headers,
    )

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 2)
    )
    second_charity_project_closed = result.scalars().first()

    await session.refresh(first_donation_amount)

    assert (
        first_donation_amount.fully_invested is True
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )
    assert (
        second_charity_project_closed.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_3",
            "description": "Project_3",
            "full_amount": 150,
        },
        headers=headers,
    )

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 3)
    )
    third_charity_project_closed = result.scalars().first()

    result = await session.execute(select(Donation).filter(Donation.id == 2))

    second_donation_amount = result.scalars().first()
    await session.refresh(first_donation_amount)

    assert (
        third_charity_project_closed.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert (
        second_donation_amount.fully_invested is True
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )


async def test_all_projects_fully_invested_and_donations_closed(
    superuser, user_client, session
):
    headers = {"Authorization": f"Bearer {superuser}"}

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": 333,
        },
        headers=headers,
    )

    user_client.post("/donation/", json={"full_amount": 100, "comment": "donation_1"})

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 1)
    )

    first_charity_project = result.scalars().first()

    result = await session.execute(select(Donation).filter(Donation.id == 1))

    first_donation_amount = result.scalars().first()
    await session.refresh(first_donation_amount)

    assert (
        first_charity_project.invested_amount == 100
    ), "Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."
    assert (
        first_donation_amount.fully_invested is True
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )

    user_client.post("/donation/", json={"full_amount": 100, "comment": "donation_2"})

    result = await session.execute(select(Donation).filter(Donation.id == 2))

    second_donation_amount = result.scalars().first()
    await session.refresh(second_donation_amount)

    await session.refresh(first_charity_project)
    await session.refresh(second_donation_amount)

    assert (
        first_charity_project.invested_amount == 200
    ), "Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."
    assert (
        second_donation_amount.fully_invested is True
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )

    user_client.post("/donation/", json={"full_amount": 200, "comment": "donation_3"})

    result = await session.execute(select(Donation).filter(Donation.id == 3))

    third_donation_amount = result.scalars().first()
    await session.refresh(third_donation_amount)
    await session.refresh(first_charity_project)

    assert (
        first_charity_project.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert (
        third_donation_amount.invested_amount == 133
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )
    assert (
        third_donation_amount.fully_invested is False
    ), (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_2",
            "description": "Project_2",
            "full_amount": 100,
        },
        headers=headers,
    )

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 2)
    )

    second_charity_project = result.scalars().first()
    await session.refresh(second_charity_project)
    await session.refresh(third_donation_amount)

    assert (
        second_charity_project.fully_invested is False
    ), "Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."
    assert second_charity_project.invested_amount == 67, (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )
    assert (
        third_donation_amount.fully_invested is True
    ), "Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."

    user_client.post("/donation/", json={"full_amount": 500, "comment": "donation_4"})

    result = await session.execute(select(Donation).filter(Donation.id == 4))

    fourth_donation_amount = result.scalars().first()
    await session.refresh(fourth_donation_amount)
    await session.refresh(second_charity_project)

    assert (
        second_charity_project.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert (
        fourth_donation_amount.invested_amount == 33
    ), f"Проверьте, что сумма пожертвования уходит в проект, открытый раньше других."

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_3",
            "description": "Project_3",
            "full_amount": 300,
        },
        headers=headers,
    )

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 3)
    )

    third_charity_project = result.scalars().first()
    await session.refresh(third_charity_project)
    await session.refresh(fourth_donation_amount)

    assert (
        third_charity_project.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert fourth_donation_amount.invested_amount == 333, (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )

    user_client.post(
        "/charity_project/",
        json={
            "name": "Project_4",
            "description": "Project_4",
            "full_amount": 167,
        },
        headers=headers,
    )

    result = await session.execute(
        select(CharityProject).filter(CharityProject.id == 4)
    )

    fourth_charity_project = result.scalars().first()
    await session.refresh(fourth_charity_project)
    await session.refresh(fourth_donation_amount)

    assert (
        fourth_charity_project.fully_invested is True
    ), "Проверьте, что при достижении требуемой суммы проект закрывается: для поля `fully_invested` устанавливается True."
    assert fourth_donation_amount.invested_amount == 500, (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно:"
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем — из последующего."
    )
    assert fourth_donation_amount.fully_invested is True, (
        "Проверьте, что сумма пожертвования правильно передаётся в проект;"
        "\nпроверьте, что пожертвования обрабатываются последовательно: "
        "сперва полностью распределяется сумма из предыдущего пожертвования, затем - из последующего."
    )
