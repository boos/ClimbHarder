from datetime import date
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, SecretStr


class Gender(str, Enum):
    male = "Male",
    female = "Female"
    non_binary = "Non-binary"


class UserIn(BaseModel):
    """ Base User Class """

    name: Optional[str] = Field(title="The name of the user.", max_length=256)
    surname: Optional[str] = Field(title="The surname of the user.", max_length=256)

    bio: Optional[str] = Field(title="The user description", max_length=512)
    sex: Optional[Gender]
    birthday: Optional[date] = Field(title="The birthday of the user in ISO 8601 format, like: 2008-09-15.")
    location: Optional[str]
    country: Optional[str]

    bouldering: Optional[bool] = Field(title="True if the user do bouldering.")
    sport_climbing: Optional[bool] = Field(title="True if the user do sport climbing.")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserOut(UserIn):
    username: str = Field(..., title="The username.", max_length=64)
    password: Optional[SecretStr] = Field(title="The ClimbHarder password.", max_length=256)

    email: EmailStr = Field(..., title="The email address of the user.")

    moonboard_username: Optional[str] = Field(title="MoonBoard username.", max_length=256)
    moonboard_password: Optional[SecretStr] = Field(title="MoonBoard password.", max_length=256)


class UserOnDB(UserIn):
    """ """

    username: str = Field(..., title="The username.", max_length=64)
    password: SecretStr = Field(..., title="The ClimbHarder password.", max_length=256)

    email: EmailStr = Field(..., title="The email address of the user.")

    moonboard_username: Optional[str] = Field(title="MoonBoard username.", max_length=256)
    moonboard_password: Optional[SecretStr] = Field(title="MoonBoard password.", max_length=256)

    class Config:
        extra = "forbid"


class UserInUpdateOnDB(UserIn):
    """ """

    password: Optional[SecretStr] = Field(title="The ClimbHarder password.", max_length=256)

    moonboard_username: Optional[str] = Field(title="MoonBoard username.", max_length=256)
    moonboard_password: Optional[SecretStr] = Field(title="MoonBoard password.", max_length=256)

    class Config:
        extra = "forbid"


