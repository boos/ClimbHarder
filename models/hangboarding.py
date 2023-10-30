from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

from models.climbings import PyObjectId


class GripType(Enum):
    FULL_CRIMP = 'full-crimp'
    HALF_CRIMP = 'half-crimp'
    OPEN_HAND_CRIMP = 'open-hand-crimp'


class HangboardingExerciseIn(BaseModel):
    """ Model to collect information regarding a hang on a hangboard."""
    time_under_tension: int = Field(title="The seconds spent hanging.", gt=0)
    expected_time_under_tension: int = Field(title="The expected time spent hanging.", gt=0)
    edge_size: int = Field(title="Edge size in milli meters.", gt=0)
    grip_type: GripType = Field(title="The grade of the boulder/route attempted.")
    weight: Optional[int] = Field(title="Added or subtracted weight.")
    when: datetime = Field(title="Date and time of when the exercise has been done.")

    class Config:
        json_encoders = {ObjectId: str}
        use_enum_values = True


class HangboardingExerciseInUpdate(HangboardingExerciseIn):
    """ Model information to enable user to change datetime when a hang happened."""
    time_under_tension: Optional[int] = Field(title="The seconds spent hanging.", gt=0)
    expected_time_under_tension: Optional[int] = Field(title="The expected time spent hanging.", gt=0)
    edge_size: Optional[int] = Field(title="Edge size in milli meters.", gt=0)
    grip_type: Optional[GripType] = Field(title="The grade of the boulder/route attempted.")
    weight: Optional[int] = Field(title="Added or subtracted weight.")
    when: Optional[datetime] = Field(title="Date and time of when the exercise has been done.")


class HangboardingExerciseOnDB(HangboardingExerciseInUpdate):
    """ Model information to enable to store data on database. """
    username: str = Field(..., title="The username.", max_length=64)

    class Config:
        json_encoders = {ObjectId: str}
        extra = "forbid"


class HangboardingExerciseOut(HangboardingExerciseIn):
    """ Model information to return data on API requests."""
    hang_id: PyObjectId = Field(default_factory=PyObjectId, alias="hang_id")
