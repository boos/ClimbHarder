import pprint

import pytest

from shared import test_user_login


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute_second():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01/02')
    assert response.status_code == 200

    expected_response = {'workouts': 1,
                         "sent_distribution": [],
                         "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 0, "total_unsent_moves": 1,
                         "total_sent_load": 0, "total_unsent_moves_load": 0.4, "total_load": 0.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute():
    # TODO check why is not working properly
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01')

    assert response.status_code == 200

    expected_response = {'workouts': 1,
                         "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 0, "total_unsent_moves": 1,
                         "total_sent_load": 0, "total_unsent_moves_load": 0.4, "total_load": 0.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01')

    assert response.status_code == 200

    expected_response = {'workouts': 1,
                         "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 0, "total_unsent_moves": 1,
                         "total_sent_load": 0, "total_unsent_moves_load": 0.4, "total_load": 0.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01')

    assert response.status_code == 200

    expected_response = {'workouts': 1,
                         "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 0, "total_unsent_moves": 1,
                         "total_sent_load": 0, "total_unsent_moves_load": 0.4, "total_load": 0.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01')

    assert response.status_code == 200

    expected_response = {'workouts': 2,
                         "sent_distribution": [["4a", 1]], "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 1, "total_unsent_moves": 1,
                         "total_sent_load": 4, "total_unsent_moves_load": 0.4, "total_load": 4.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()
    assert {'grade': '4a', 'load': 4, 'sent': True}.items() <= response.json()['2022-01-02']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022')
    assert response.status_code == 200

    pprint.pp(response.json())

    expected_response = {'workouts': 2,
                         "sent_distribution": [["4a", 1]], "unsent_moves_distribution": [["4a", 1]],
                         "total_sent": 1, "total_unsent_moves": 1,
                         "total_sent_load": 4, "total_unsent_moves_load": 0.4, "total_load": 4.4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['2022-01-01']['climbings'][0].items()
    assert {'grade': '4a', 'load': 4, 'sent': True}.items() <= response.json()['2022-01-02']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_latest_workout():
    ac = await test_user_login()

    response = await ac.get('/workouts/latest')
    assert response.status_code == 200

    expected_response = {'workouts': 1,
                         "sent_distribution": [["4a", 1]],
                         "total_sent": 1, "total_unsent_moves": 0,
                         "total_sent_load": 4, "total_unsent_moves_load": 0, "total_load": 4}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 4, 'sent': True}.items() <= response.json()['2022-01-02']['climbings'][0].items()


@pytest.mark.anyio
async def test_can_successfully_delete_climbing_exercise_from_workouts():
    ac = await test_user_login()
    response = await ac.get('/workouts')
    assert response.status_code == 200
    response_data = response.json()

    for key in response_data:

        if key.find('-') == -1:
            continue

        for climbing in response_data[key]['climbings']:
            response = await ac.delete('/climbings/{}'.format(climbing['climb_id']))
            assert response.status_code == 200
