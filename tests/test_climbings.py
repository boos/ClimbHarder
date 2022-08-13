import datetime
import json

import pytest

from tests.shared import test_user_login


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_now():
    ac = await test_user_login()

    data = {"grade": "6a", "sent": True}
    response = await ac.post('/climbings/now', content=json.dumps(data))
    assert response.json()['load'] == 6.0
    assert response.status_code == 201
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_now():
    ac = await test_user_login()

    data = {"grade": "6a", "moves": 1, "total_moves": 10, "sent": False}
    response = await ac.post('/climbings/now', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 0.6
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "sent": True}
    response = await ac.post('/climbings/2022/01/01/01/01/01', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 4
    assert response.json()['when'].__str__() == datetime.datetime(2022, 1, 1, 1, 1, 1).isoformat()
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "moves": 1, "total_moves": 10, "sent": False}
    response = await ac.post('/climbings/2022/01/01/01/01/02', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 0.4
    assert response.json()['when'].__str__() == datetime.datetime(2022, 1, 1, 1, 1, 2).isoformat()
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_change_a_climbing_exercise_in_a_workout():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_delete_a_climbing_exercise_in_a_workout():
    # TODO
    ac = await test_user_login()
