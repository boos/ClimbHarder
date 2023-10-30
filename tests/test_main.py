import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from routers import users, security

app.include_router(users.router)
app.include_router(security.router)

client = TestClient(app, base_url="http://127.0.0.1:8000")


@pytest.mark.anyio
async def test_read_root():
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    response = await ac.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "I am ClimbHarder, and I will make you climb HARDER!"}
