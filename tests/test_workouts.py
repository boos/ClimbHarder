import json

import pytest

from shared import test_user_login


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_now():
    ac = await test_user_login()

    data = {"grade": "4a", "sent": True}
    response = await ac.post('/workout/now', content=json.dumps(data))
    # assert response.status_code == 422
    # assert response.json() == {}


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_now():
    ac = await test_user_login()

    data = {"grade": "4a", "moves": 0, "total_moves": 0, "sent": False}
    response = await ac.post('/workout/now', content=json.dumps(data))
    # assert response.status_code == 422
    # assert response.json() == {}


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "sent": True}
    response = await ac.post('/workout/now', content=json.dumps(data))
    # assert response.status_code == 422
    # assert response.json() == {}


@pytest.mark.anyio
async def test_can_successfully_add_climbing_exercise_to_workout_no_sent_when():
    ac = await test_user_login()

    data = {"grade": "4a", "moves": 0, "total_moves": 0, "sent": False}
    response = await ac.post('/workout/now', content=json.dumps(data))
    # assert response.status_code == 422
    # assert response.json() == {}


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute_second():
    # TODO
    ac = await test_user_login()

    data = {"grade": "4a", "moves": 0, "total_moves": 0, "sent": True}


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour_minute():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day_hour():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month_day():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year_month():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout_year():
    # TODO
    ac = await test_user_login()


@pytest.mark.anyio
async def test_can_successfully_get_climbing_exercise_from_workout():
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
