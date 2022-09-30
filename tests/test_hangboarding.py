import datetime
import json

import pytest

from tests.shared import test_user_login

hang_id = 0


@pytest.mark.anyio
async def test_can_successfully_add_a_hangboarding_exercise_to_a_workout():
    ac = await test_user_login()

    data = {
        "time_under_tension": 10,
        "expected_time_under_tension": 10,
        "edge_size": 10,
        "grip_type": "full-crimp",
        "weight": 10,
        "when": "2022-01-01T1:2:2"
    }
    response = await ac.post('/hangboarding', content=json.dumps(data))
    response_d = response.json()

    assert response.status_code == 201
    assert response_d['time_under_tension'] == 10
    assert response_d['expected_time_under_tension'] == 10
    assert response_d['edge_size'] == 10
    assert response_d['grip_type'] == 'full-crimp'
    assert response_d['weight'] == 10
    assert response_d['when'] == '2022-01-01T01:02:02'

    global hang_id
    hang_id = response_d['hang_id']


@pytest.mark.anyio
async def test_can_successfully_patch_a_hangboarding_exercise_to_a_workout():
    ac = await test_user_login()

    data = {'time_under_tension': 20}
    response = await ac.patch('/hangboarding/{}'.format(hang_id), content=json.dumps(data))
    response_d = response.json()

    assert response.status_code == 200
    assert response_d['time_under_tension'] == 20
    assert response_d['expected_time_under_tension'] == 10
    assert response_d['edge_size'] == 10
    assert response_d['grip_type'] == 'full-crimp'
    assert response_d['weight'] == 10
    assert response_d['when'] == '2022-01-01T01:02:02'


@pytest.mark.anyio
async def test_can_successfully_delete_a_hangboarding_exercise_in_a_workout():
    ac = await test_user_login()
    response = await ac.delete('/hangboarding/{}'.format(hang_id))
    response_d = response.json()

    assert response.status_code == 200
    # hang_id is not in response when hangboard exercise is successfully deleted
    deleted = 'hang_id' not in response_d
    assert deleted == True
    assert response_d['time_under_tension'] == 20
    assert response_d['expected_time_under_tension'] == 10
    assert response_d['edge_size'] == 10
    assert response_d['grip_type'] == 'full-crimp'
    assert response_d['weight'] == 10
    assert response_d['when'] == '2022-01-01T01:02:02'
