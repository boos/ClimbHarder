from misc import nosql
from fastapi.testclient import TestClient
from routers import users, security

from main import app

app.include_router(users.router)
app.include_router(security.router)

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "I am ClimbHarder, and I will make you climb HARDER!"}