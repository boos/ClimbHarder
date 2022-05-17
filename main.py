from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from routers import users, security

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(users.router)
app.include_router(security.router)


@app.get("/")
async def root():
    return {"message": "I am ClimbHarder, and I will make you climb HARDER!"}
