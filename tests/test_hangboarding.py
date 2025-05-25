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
        "when": "2025-05-25T21:48:43.913Z"
    }
    response = await ac.post('/hangboarding', content=json.dumps(data))
    response_d = response.json()

    assert response.status_code == 201
    assert response_d['time_under_tension'] == 10
    assert response_d['expected_time_under_tension'] == 10
    assert response_d['edge_size'] == 10
    assert response_d['grip_type'] == 'full-crimp'
    assert response_d['weight'] == 10
    assert response_d['when'] == '2025-05-25T21:48:43.913000Z'

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
    assert response_d['when'] == '2025-05-25T21:48:43.913000'


@pytest.mark.anyio
async def test_can_successfully_delete_a_hangboarding_exercise_in_a_workout():
    ac = await test_user_login()
    response = await ac.delete('/hangboarding/{}'.format(hang_id))
    response_d = response.json()

    assert response.status_code == 200
    # hang_id is not in response when hangboard exercise is successfully deleted
    assert response_d['time_under_tension'] == 20
    assert response_d['expected_time_under_tension'] == 10
    assert response_d['edge_size'] == 10
    assert response_d['grip_type'] == 'full-crimp'
    assert response_d['weight'] == 10
    assert response_d['when'] == '2025-05-25T21:48:43.913000'
