from datetime import datetime

import pymongo.errors
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from pymongo import ReturnDocument

import misc.security
from misc import nosql
from misc.nosql import users_collection
from misc.security import oauth2_scheme
from models.users import UserOnDB, UserOut, UserInUpdateOnDB

router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.post("/users",
             response_model=UserOut,
             response_model_exclude_defaults=True,
             response_model_exclude_unset=True,
             response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: UserOnDB):
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

    # TODO: ensure that users can only be created after email verification

    user.password = misc.security.get_password_hash(user.password.get_secret_value())
    if user.birthday:
        user.birthday = datetime.combine(user.birthday, datetime.min.time())

    try:

        await nosql.db["users"].insert_one(user.dict(exclude_none=True, exclude_defaults=True, exclude_unset=True))

    except pymongo.errors.DuplicateKeyError as err:

        if err.__str__().find("username") != -1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Username already in use, choose another username.")

        if err.__str__().find("email") != -1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already in use, choose another email.")
    return user


@router.get("/users/me",
            response_model=UserOut,
            response_model_exclude_defaults=True,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            )
async def get_my_user_details(current_user: dict = Depends(misc.security.get_current_user)):
    return current_user


@router.get("/users/{username}",
            response_model=UserOut,
            response_model_exclude_defaults=True,
            response_model_exclude_unset=True,
            response_model_exclude_none=True)
async def get_other_user_details(username: str):

    user = await users_collection.find_one({"username":  username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username not found.",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


@router.delete("/users/me")
async def delete_user(current_user: dict = Depends(misc.security.get_current_user)):

    response_status = await users_collection.delete_one({"username": current_user['username']})
    if response_status.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to delete '{}': User not found.".format(current_user['username']),
                            headers={"WWW-Authenticate": "Bearer"})

    return {"message: {} deleted.".format(current_user['username'])}


@router.patch("/users/me",
              response_model=UserOut,
              response_model_exclude_defaults=True,
              response_model_exclude_unset=True,
              response_model_exclude_none=True)
async def patch_user_details(user: UserInUpdateOnDB, current_user: dict = Depends(misc.security.get_current_user)):

    if user.password:
        user.password = misc.security.get_password_hash(user.password.get_secret_value())

    if user.moonboard_password:
        user.moonboard_password = user.moonboard_password.get_secret_value()

    if user.birthday:
        user.birthday = datetime.combine(user.birthday, datetime.min.time())

    try:
        user_from_db = await users_collection.find_one_and_update({"username": current_user['username']},
                                                                  {"$set": user.dict(exclude_none=True,
                                                                                     exclude_defaults=True,
                                                                                     exclude_unset=True)},
                                                                  return_document=ReturnDocument.AFTER)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to update '{}': User not found.".format(current_user['username']),
                            headers={"WWW-Authenticate": "Bearer"})

    return user_from_db
