from pprint import pprint

import pymongo.errors
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from misc import nosql
from models.users import UserIn, UserOut
from routers import security

router = APIRouter()


@router.get("/users")
async def users():
    return {"message": f"all users returned."}


@router.post("/user", response_model=UserOut,response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn):
    """
    Create a user with all the information:

    - **username**: each user must have a unique username
    - **password**: each username must have a password

    - **name**: each user might define his/her real name
    - **surname**: each user might define his/her surname
    - **email**: each user might have a valid email address
    - **bio**: each user might have a biographic field
    - **sex**: each user might define his/her sex between male/female/non-binary

    - **birthday**: each user might define his/her sex between male/female/non-binary
    - **location**: each user might define his/her location
    - **country**: each user might define his/her country

    - **bouldering**: each user might define if he/she does bouldering
    - **sport_climbing**: each user might define if he/she does sport climbing

    - **moonboard_username**: each user might define he/she moonboard username
    - **moonboard_username**: each user might define he/she moonboard password
    """

    user.password = security.get_password_hash(user.password.__str__())

    try:
        new_user = await nosql.db["users"].insert_one(jsonable_encoder(user,
                                                                       exclude_none=True,
                                                                       exclude_unset=True,
                                                                       exclude_defaults=True))
    except pymongo.errors.DuplicateKeyError as err:
        if err.__str__().find("username") != -1:
            raise HTTPException(status_code=409, detail="Username already in use, choose another username.")
        if err.__str__().find("email") != -1:
            raise HTTPException(status_code=409, detail="Email already in use, choose another email.")
    return user


# @router.get("/user/me", response_model=UserOut, response_model_exclude_unset=True)
# async def my_user_details(current_user: UserOut = Depends(security.get_current_user)):
#     return current_user


@router.delete("/user/{username}")
async def delete_user(username: str):
    return {"message": f"{username} deleted."}


@router.get("/user/{username}")
async def user_details(username: str):
    return {"message": f"{username} details."}


@router.put("/user/{username}", response_model=UserOut, response_model_exclude_unset=True)
async def update_user(username: str):
    return {"message": f"{username} updated."}
