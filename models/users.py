from datetime import date
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, SecretStr


class Gender(str, Enum):
    male = "Male",
    female = "Female"
    non_binary = "Non-binary"


class User(BaseModel):

    username: str = Field(..., title="The username.", max_length=64)
    email: EmailStr = Field(..., title="The email address of the user.")

    name: Optional[str] = Field(None, title="The name of the user.", max_length=256)
    surname: Optional[str] = Field(None, title="The surname of the user.", max_length=256)

    bio: Optional[str] = Field(None, title="The user description", max_length=512)
    sex: Optional[Gender] = None
    birthday: Optional[date] = Field("1900-01-01", title="The birthday of the user.")
    location: Optional[str] = None
    country: Optional[str] = None

    bouldering: Optional[bool] = Field(False, title="True if the user do bouldering.")
    sport_climbing: Optional[bool] = Field(False, title="True if the user do sport climbing.")

    moonboard_username: Optional[str] = Field(None, title="MoonBoard username.", max_length=256)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserIn(User):

    password: SecretStr = Field(..., title="The ClimbHarder username password.", max_length=256)
    moonboard_password: Optional[SecretStr] = Field(None, title="MoonBoard password.", max_length=256)


class UserOut(User):
    pass
