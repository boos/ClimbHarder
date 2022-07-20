from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class FontBoulderingGrade(Enum):
    F_4A = "4a"
    F_4A_PLUS = "4a+"
    F_4B = "4b"
    F_4B_PLUS = "4b+"
    F_4C = "4c"
    F_4C_PLUS = "4c+"

    F_5A = "5a"
    F_5A_PLUS = "5a+"
    F_5B = "5b"
    F_5B_PLUS = "5b+"
    F_5C = "5c"
    F_5C_PLUS = "5c+"

    F_6A = "6a"
    F_6A_PLUS = "6a+"
    F_6B = "6b"
    F_6B_PLUS = "6b+"
    F_6C = "6c"
    F_6C_PLUS = "6c+"

    F_7A = "7a"
    F_7A_PLUS = "7a+"
    F_7B = "7b"
    F_7B_PLUS = "7b+"
    F_7C = "7c"
    F_7C_PLUS = "7c+"

    F_8A = "8a"
    F_8A_PLUS = "8a+"
    F_8B = "8b"
    F_8B_PLUS = "8b+"
    F_8C = "8c"
    F_8C_PLUS = "8c+"

    F_9A = "9a"
    F_9A_PLUS = "9a+"
    F_9B = "9b"
    F_9B_PLUS = "9b+"
    F_9C = "9c"
    F_9C_PLUS = "9c+"


class ClimbingExerciseIn(BaseModel):
    """ Collect basic information regarding a climb """
    grade: FontBoulderingGrade = Field(title="The grade of the boulder/route attempted.")
    moves: Optional[int] = Field(title="The number of moves successfully done.", gt=0)
    total_moves: Optional[int] = Field(title="The total number of moves of the boulder/route attempted.", gt=0)
    sent: bool = Field(title="True if you sent the boulder/route.")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class ClimbingExerciseOut(ClimbingExerciseIn):

    load: float = Field(title='The estimated load of the exercise.')
    when: datetime = Field(title="Date and time of when the exercise has been done.")


class ClimbingExerciseOnDB(ClimbingExerciseOut):

    username: str = Field(..., title="The username.", max_length=64)

    class Config:
        use_enum_values = True

