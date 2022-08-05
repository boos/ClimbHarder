from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from routers import users, security, workouts

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(users.router)
app.include_router(security.router)
app.include_router(workouts.router)


@app.get("/")
async def root():
    # return "/docs"
    return {"message": "I am ClimbHarder, and I will make you climb HARDER!"}
