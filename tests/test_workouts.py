import datetime

import pytest

from shared import test_user_login


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute_second():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01/01')
    assert response.status_code == 200

    expected_response = {'distribution_of_climbing_exercises': {'4a': {'sent': 1}}, 'total_load': 4.0, 'total_sent': 1}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '4a', 'load': 4.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute():
    ac = await test_user_login()

    response = await ac.get('/workouts/2022/01/01/01/01')
    assert response.status_code == 200

    expected_response = {'distribution_of_climbing_exercises': {'4a': {'moves': [[1, 10]], 'sent': 1}}, 'total_load': 4.4, 'total_sent': 1, 'total_unsent_moves': 1}

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

    expected_response = {'distribution_of_climbing_exercises': {'6a': {'moves': [[1, 10]], 'sent': 1}}, 'total_load': 6.6, 'total_sent': 1, 'total_unsent_moves': 1}

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

    expected_response = {'distribution_of_climbing_exercises': {'6a': {'moves': [[1, 10]], 'sent': 1}}, 'total_load': 6.6, 'total_sent': 1, 'total_unsent_moves': 1}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '6a', 'load': 6.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '6a', 'load': 0.6, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}/{}'.format(datetime.datetime.now().year,
                                                     datetime.datetime.now().month))

    assert response.status_code == 200

    expected_response = {'distribution_of_climbing_exercises': {'6a': {'moves': [[1, 10]], 'sent': 1}}, 'total_load': 6.6, 'total_sent': 1, 'total_unsent_moves': 1}

    assert expected_response.items() <= response.json().items()
    assert {'grade': '6a', 'load': 6.0, 'sent': True}.items() <= response.json()['climbing_exercises'][0].items()
    assert {'grade': '6a', 'load': 0.6, 'sent': False}.items() <= response.json()['climbing_exercises'][1].items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year():
    ac = await test_user_login()

    response = await ac.get('/workouts/{}'.format(datetime.datetime.now().year))

    assert response.status_code == 200

    expected_response = {'distribution_of_climbing_exercises': {'4a': {'sent': 1, 'moves': [[1, 10]]},
                                                               '6a': {'sent': 1, 'moves': [[1, 10]]}}, 'total_load': 11.0, 'total_sent': 2, 'total_unsent_moves': 2}

    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_from_sent_to_nosent():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_from_nosent_to_sent():
    # TODO
    ac = await test_user_login()
