from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routers import users, security, workouts

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(users.router)
app.include_router(security.router)
app.include_router(workouts.router)


@app.on_event("startup")
async def application_initialization():
    from misc.nosql import mongodb_initialization
    await mongodb_initialization()


@app.get("/")
async def root():
    # return "/docs"
    return {"message": "I am ClimbHarder, and I will make you climb HARDER!"}
