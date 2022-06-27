import datetime

from fastapi import APIRouter, Depends, status

from misc import security, exercises_climbing
from models.exercises_climbing import ClimbingExerciseIn, ClimbingExerciseOut

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])


@router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, day, hour, minute, current_user: dict = Depends(security.get_current_user)):
    """ Return info about the specified workout """
    return year, month, day, hour, minute, current_user


@router.post("/workouts/{year}/{month}/{day}/{hour}/{minute}",
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_climbing_exercise_to_workout(year, month, day, hour, minute,
                                           climbing_exercise: ClimbingExerciseIn,
                                           current_user: dict = Depends(security.get_current_user)):
    """ TODO: Add a climbing exercise to a specific workout """

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)
    climbing_exercise_out = ClimbingExerciseOut(grade=climbing_exercise.grade, moves=climbing_exercise.moves,
                                                total_moves=climbing_exercise.total_moves, sent=climbing_exercise.sent,
                                                load=load)

    return climbing_exercise_out
