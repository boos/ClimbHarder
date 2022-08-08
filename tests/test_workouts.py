import datetime
import json

import pytest

from shared import test_user_login


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_now():
    ac = await test_user_login()

    data = {"grade": "6a", "sent": True}
    response = await ac.post('/workouts/now', content=json.dumps(data))
    assert response.json()['load'] == 6.0
    assert response.status_code == 201
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_now():
    ac = await test_user_login()

    data = {"grade": "6a", "moves": 1, "total_moves": 10, "sent": False}
    response = await ac.post('/workouts/now', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 0.6
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "sent": True}
    response = await ac.post('/workouts/2022/01/01/01/01/01', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 4
    assert response.json()['when'].__str__() == datetime.datetime(2022, 1, 1, 1, 1, 1).isoformat()
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "moves": 1, "total_moves": 10, "sent": False}
    response = await ac.post('/workouts/2022/01/01/01/01/02', content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['load'] == 0.4
    assert response.json()['when'].__str__() == datetime.datetime(2022, 1, 1, 1, 1, 2).isoformat()
    assert data.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute_second():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01/01')
    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'4a': {'sent': 1}}
    expected_response['total_load'] = 4.0
    expected_response['total_sent'] = 1

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 4.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01')
    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'4a': {'moves': [[1, 10]], 'sent': 1}}
    expected_response['total_load'] = 4.4
    expected_response['total_sent'] = 1
    expected_response['total_unsent_moves'] = 1

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 4.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '4a', 'load': 0.4, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}/{}/{}/{}'.format(datetime.datetime.now().year,
                                                           datetime.datetime.now().month,
                                                           datetime.datetime.now().day,
                                                           datetime.datetime.now().hour))
    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'6a': {'moves': [[1, 10]], 'sent': 1}}
    expected_response['total_load'] = 6.6
    expected_response['total_sent'] = 1
    expected_response['total_unsent_moves'] = 1

    assert expected_response.items() <= response.json().items()
    assert {'grade': '6a', 'load': 6.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '6a', 'load': 0.6, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}/{}/{}'.format(datetime.datetime.now().year,
                                                        datetime.datetime.now().month,
                                                        datetime.datetime.now().day))
    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'6a': {'moves': [[1, 10]], 'sent': 1}}
    expected_response['total_load'] = 6.6
    expected_response['total_sent'] = 1
    expected_response['total_unsent_moves'] = 1

    assert expected_response.items() <= response.json().items()
    assert {'grade': '6a', 'load': 6.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '6a', 'load': 0.6, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}/{}'.format(datetime.datetime.now().year,
                                                     datetime.datetime.now().month))

    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'6a': {'moves': [[1, 10]], 'sent': 1}}
    expected_response['total_load'] = 6.6
    expected_response['total_sent'] = 1
    expected_response['total_unsent_moves'] = 1

    assert expected_response.items() <= response.json().items()
    assert {'grade': '6a', 'load': 6.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '6a', 'load': 0.6, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}'.format(datetime.datetime.now().year))

    assert response.status_code == 200

    expected_response = dict()
    expected_response['distribution_of_climbing_exercises'] = {'4a': {'sent': 1, 'moves': [[1, 10]]},
                                                               '6a': {'sent': 1, 'moves': [[1, 10]]}}
    expected_response['total_load'] = 11.0
    expected_response['total_sent'] = 2
    expected_response['total_unsent_moves'] = 2

    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_from_sent_to_nosent():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_from_nosent_to_sent():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_change_a_climbing_exercise_in_a_workout():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_delete_a_climbing_exercise_in_a_workout():
    # TODO
    ac = await test_user_login()
