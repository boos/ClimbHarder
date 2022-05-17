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




# async def test_negative_authenticate():
#     # username: SHA1(testing),
#     # password: SHA1(testdriven)
#     response = await security.authenticate_user('dc724af18fbdd4e59189f5fe768a5f8311527050',
#                                                 'wrongpassword')
#     assert response is False
