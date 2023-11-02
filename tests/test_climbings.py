import datetime
import json
import pprint

import pytest

from tests.shared import test_user_login

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
async def test_can_successfully_patch_climbing_exercise_from_workout_from_sent_to_nosent():
    ac = await test_user_login()
    response = await ac.get('/workouts/2022/01/01/01/01/01')
    assert response.status_code == 200
    id = response.json()['2022-01-01']['climbings'][0]['climb_id']

    data = {"grade": "4a", "moves": 1, "total_moves": 10, "sent": False}
    data = json.dumps(data)
    response = await ac.patch('/climbings/{}'.format(id), content=data)

    assert response.status_code == 200
    assert response.json()['load'] == 0.4


@pytest.mark.anyio
async def test_can_successfully_patch_climbing_exercise_from_workout_from_nosent_to_sent():
    ac = await test_user_login()
    response = await ac.get('/workouts/2022/01/01/01/01/01')
    assert response.status_code == 200
    id = response.json()['2022-01-01']['climbings'][0]['climb_id']

    data = {"grade": "4a", "sent": True}
    data = json.dumps(data)
    response = await ac.patch('/climbings/{}'.format(id), content=data)

    assert response.status_code == 200
    assert response.json()['load'] == 4.0


@pytest.mark.anyio
async def test_can_successfully_patch_climbing_exercise_from_workout_changing_when():
    ac = await test_user_login()
    response = await ac.get('/workouts/2022/01/01/01/01/01')
    assert response.status_code == 200
    id = response.json()['2022-01-01']['climbings'][0]['climb_id']

    data = {"grade": "4a", "sent": True, "when": "2022-01-02T01:01:10"}
    data = json.dumps(data)
    response = await ac.patch('/climbings/{}'.format(id), content=data)

    assert response.status_code == 200
    assert response.json()['when'] == "2022-01-02T01:01:10"

    data = {"grade": "4a", "sent": True, "when": "2022-01-02T01:01:01"}
    data = json.dumps(data)
    response = await ac.patch('/climbings/{}'.format(id), content=data)

    assert response.status_code == 200
    assert response.json()['when'] == "2022-01-02T01:01:01"
