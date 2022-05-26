import pytest
import json
from httpx import AsyncClient

from main import app


async def test_user_login(username='test', password='test') -> AsyncClient:
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    response = await ac.post("/token", data={'username': username, 'password': password})
    assert response.status_code == 200
    ac.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    return ac


@pytest.mark.anyio
async def test_cannot_create_user_without_username_email_password():
    ac = await test_user_login()

    data = {}
    response = await ac.post('/user', content=json.dumps(data))
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': [
        'body', 'email'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.anyio
async def test_cannot_create_user_existing_username():
    ac = await test_user_login()

    data = {'username': 'test', 'password': 'test', 'email': 'rmartelloni+test@gmail.com'}
    response = await ac.post('/user', content=json.dumps(data))
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
    response = await ac.post('/user', content=json.dumps(data))

    assert response.status_code == 409
    assert response.json() == {'detail': 'Email already in use, choose another email.'}


@pytest.mark.anyio
async def test_can_successfully_create_user():
    ac = await test_user_login()

    data = {'username': 'test-1', 'password': 'test-1', 'email': 'rmartelloni+test-1@gmail.com'}
    response = await ac.post('/user', content=json.dumps(data))

    assert response.status_code == 201
    assert response.json() == {'email': 'rmartelloni+test-1@gmail.com', 'username': 'test-1'}


@pytest.mark.anyio
async def test_cannot_delete_other_user_if_not_admin():
    ac = await test_user_login('test', 'test')

    response = await ac.delete('/user/{}'.format('test-3'))

    assert response.status_code == 401
    assert response.json() == {'detail': "Unable to delete 'test-3': Unauthorized."}


@pytest.mark.anyio
async def test_can_delete_user_self():
    ac = await test_user_login('test-1', 'test-1')

    response = await ac.delete('/user/{}'.format('test-1'))

    assert response.status_code == 200
    assert response.json() == ['message: test-1 deleted.']


@pytest.mark.anyio
async def test_can_successfully_delete_other_user_if_admin():
    ac = await test_user_login('iRockClimb', 'climbing')

    data = {'username': 'test-3', 'password': 'test-3', 'email': 'rmartelloni+test-3@gmail.com'}
    response = await ac.post('/user', content=json.dumps(data))

    assert response.status_code == 201
    assert response.json() == {'email': 'rmartelloni+test-3@gmail.com', 'username': 'test-3'}

    response = await ac.delete('/user/{}'.format('test-3'))

    assert response.status_code == 200
    assert response.json() == ['message: test-3 deleted.']


def test_can_get_my_user_details():
    pass


def test_cannot_update_other_user_details():
    pass


def test_update_user_details_if_self():
    pass


def test_cannot_get_other_user_details_if_not_public():
    pass
