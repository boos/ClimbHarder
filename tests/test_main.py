from fastapi.testclient import TestClient

from main import app
from routers import users, security

app.include_router(users.router)
app.include_router(security.router)

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "I am ClimbHarder, and I will make you climb HARDER!"}
