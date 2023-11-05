from httpx import AsyncClient
from main import app
from dotenv import load_dotenv

load_dotenv()


async def test_user_login(username='test', password='test') -> AsyncClient:
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    response = await ac.post("/token", data={'username': username, 'password': password})
    assert response.status_code == 200
    ac.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    return ac
