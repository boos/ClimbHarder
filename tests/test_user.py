import json

import pytest

from shared import test_user_login


@pytest.mark.anyio
async def test_cannot_create_user_without_username_email_password():
    ac = await test_user_login()

    data = {}
    response = await ac.post('/users', content=json.dumps(data))
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'email'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.anyio
async def test_cannot_create_user_existing_username():
    ac = await test_user_login()

    data = {'username': 'test', 'password': 'test', 'email': 'rmartelloni+test@gmail.com'}
    response = await ac.post('/users', content=json.dumps(data))
    assert response.status_code == 409
    assert response.json() == {'detail': 'Username already in use, choose another username.'}


@pytest.mark.anyio
async def test_cannot_create_user_existing_email():
    ac = await test_user_login()

    import random
    import string

    # printing lowercase
    letters = string.ascii_lowercase
    random_username = ''.join(random.choice(letters) for i in range(64))

    data = {'username': random_username, 'password': 'test', 'email': 'rmartelloni+test@gmail.com'}
    response = await ac.post('/users', content=json.dumps(data))

    assert response.status_code == 409
    assert response.json() == {'detail': 'Email already in use, choose another email.'}


@pytest.mark.anyio
async def test_can_successfully_create_user():
    ac = await test_user_login()

    data = {'username': 'test-1', 'password': 'test-1', 'email': 'rmartelloni+test-1@gmail.com', }
    response = await ac.post('/users', content=json.dumps(data))

    assert response.status_code == 201
    assert response.json() == {'email': 'rmartelloni+test-1@gmail.com', 'password': '**********','username': 'test-1'}


@pytest.mark.anyio
async def test_can_successfully_delete_user_self():
    ac = await test_user_login('test-1', 'test-1')

    response = await ac.delete('/users/me'.format('test-1'))

    assert response.status_code == 200
    assert response.json() == ['message: test-1 deleted.']


@pytest.mark.anyio
async def test_can_successfully_get_my_user_details():
    ac = await test_user_login()

    response = await ac.get('/users/me')
    data = response.json()

    assert response.status_code == 200
    assert data['email'] == 'rmartelloni+test@gmail.com'
    assert data['password'] == '**********'
    assert data['username'] == 'test'


@pytest.mark.anyio
async def test_can_successfully_get_other_user_details():

    ac = await test_user_login()

    response = await ac.get('/users/rmartelloni')

    assert response.status_code == 200
    assert response.json()['username'] == 'rmartelloni'


@pytest.mark.anyio
async def test_can_successfully_update_user_details():
    ac = await test_user_login()

    data = {
        "name": "Climbing",
        "surname": "Machine",
        "bio": "Incredible Climbing Machine",
        "sex": "Male",
        "birthday": "2020-09-15",
        "location": "Zurich",
        "country": "Switzerland",
        "bouldering": True,
        "sport_climbing": False,
        "moonboard_username": "Ponzio",
        "moonboard_password": "Pilato"
    }

    response = await ac.patch('/users/me', content=json.dumps(data))

    response = await ac.get('/users/me')
    data = response.json()

    data['username'] = 'test'
    data['password'] = '**********'
    data['name'] = 'Climbing'
    data['surname'] = "Machine"
    data['moonboard_password'] = '**********'
    data['email'] = 'rmartelloni+test@gmail.com'
    assert response.status_code == 200
    assert response.json() == data
