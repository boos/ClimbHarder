from pprint import pprint

from httpx import AsyncClient
from jose import jwt

import misc.security
from main import app
from routers import security

from tests.shared import test_user_login


async def test_authenticate_wrong_username_password():
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    response = await ac.post("/token", data={'username': 'dc724af18fbdd4e59189f5fe768a5f8311527050+wrong',
                                             'password':'wrong-password'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid username or password'}


async def test_authenticate_right_username_wrong_password():
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    response = await ac.post("/token", data={'username': 'test',
                                             'password': 'test+wrong-password'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid username or password'}


async def test_authenticate_right_username_right_password():
    await test_user_login()


def test_can_create_access_token_successfully():
    user = {'username': 'test_user', 'password': 'test_password'}
    access_token = misc.security.create_access_token(data={"sub": user['username']})

    creds = jwt.decode(access_token, str(misc.security.SECRET_KEY), algorithms=[misc.security.ALGORITHM])
    pprint(creds)
    assert creds.get("sub") is not None
    assert creds["sub"] == user['username']
