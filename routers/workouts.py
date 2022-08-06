import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException
from pymongo import ReturnDocument

from misc import security, exercises_climbing, nosql
from misc.exercises_climbing import build_workout_details
from models.exercises_climbing import ClimbingExerciseIn, ClimbingExerciseInUpdateOnDB
from models.exercises_climbing import ClimbingExerciseOut, ClimbingExerciseOnDB

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])


@router.get("/workouts/{year}/{month}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month. """

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'},
                                                                         'month': {'$month': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)},
                                                                       'month': {'$eq': int(month)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


@router.get("/workouts/{year}/{month}/{day}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, day, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day """

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'},
                                                                         'month': {'$month': '$when'},
                                                                         'day': {'$dayOfMonth': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)},
                                                                       'month': {'$eq': int(month)},
                                                                       'day': {'$eq': int(day)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


@router.get("/workouts/{year}/{month}/{day}/{hour}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, day, hour, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour """

    when = datetime.datetime(int(year), int(month), int(day), int(hour))

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'},
                                                                         'month': {'$month': '$when'},
                                                                         'day': {'$dayOfMonth': '$when'},
                                                                         'hour': {'$hour': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)},
                                                                       'month': {'$eq': int(month)},
                                                                       'day': {'$eq': int(day)},
                                                                       'hour': {'$eq': int(hour)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


@router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, day, hour, minute, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour, and minute """

    when = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'},
                                                                         'month': {'$month': '$when'},
                                                                         'day': {'$dayOfMonth': '$when'},
                                                                         'hour': {'$hour': '$when'},
                                                                         'minute': {'$minute': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)},
                                                                       'month': {'$eq': int(month)},
                                                                       'day': {'$eq': int(day)},
                                                                       'hour': {'$eq': int(hour)},
                                                                       'minute': {'$eq': int(minute)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


# TODO: add get with seconds
# @router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}", status_code=status.HTTP_200_OK)
# async def get_workout_details(year, month, day, hour, minute, second,
# current_user: dict = Depends(# security.get_current_user)):


@router.post("/workouts",
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_climbing_exercise_to_workout(climbing_exercise: ClimbingExerciseIn,
                                           current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to a specific workout done now """

    when = datetime.datetime.now()

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)

    climbing_exercise_out_on_db = ClimbingExerciseOnDB(grade=climbing_exercise.grade.value,
                                                       moves=climbing_exercise.moves,
                                                       total_moves=climbing_exercise.total_moves,
                                                       sent=climbing_exercise.sent,
                                                       load=load,
                                                       when=when,
                                                       username=current_user['username'])

    await nosql.workouts_collection.insert_one(climbing_exercise_out_on_db.dict(exclude_none=True,
                                                                                exclude_unset=True,
                                                                                exclude_defaults=True))
    return climbing_exercise_out_on_db


@router.post('/workouts/{year}/{month}/{day}/{hour}/{minute}/{second}',
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_climbing_exercise_to_workout(climbing_exercise: ClimbingExerciseIn,
                                           year, month, day, hour, minute, second,
                                           current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to the year, month, day, hour and minute workout. """

    when = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)

    climbing_exercise_out_on_db = ClimbingExerciseOnDB(grade=climbing_exercise.grade.value,
                                                       moves=climbing_exercise.moves,
                                                       total_moves=climbing_exercise.total_moves,
                                                       sent=climbing_exercise.sent,
                                                       load=load,
                                                       when=when,
                                                       username=current_user['username'])

    await nosql.workouts_collection.insert_one(climbing_exercise_out_on_db.dict(exclude_none=True,
                                                                                exclude_unset=True,
                                                                                exclude_defaults=True))

    return climbing_exercise_out_on_db


# TODO: create router.post with minute only


@router.patch("/workouts/{object_id}/",
              response_model=ClimbingExerciseOut,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK)
async def update_a_climbing_exercise_in_a_workout(climbing_exercise: ClimbingExerciseInUpdateOnDB, object_id,
                                                  current_user: dict = Depends(security.get_current_user)):
    """ Update and return an exercise referenced by the object_id """

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)

    climbing_exercise_out_on_db = ClimbingExerciseOnDB(grade=climbing_exercise.grade.value,
                                                       moves=climbing_exercise.moves,
                                                       total_moves=climbing_exercise.total_moves,
                                                       sent=climbing_exercise.sent,
                                                       load=load,
                                                       when=climbing_exercise.when,
                                                       username=current_user['username'])

    response = await nosql.workouts_collection.find_one_and_update({"_id": ObjectId(object_id),
                                                                    "username": current_user['username']},
                                                                   {"$set": climbing_exercise_out_on_db.dict(
                                                                       exclude_none=True,
                                                                       exclude_defaults=True,
                                                                       exclude_unset=True)},
                                                                   return_document=ReturnDocument.AFTER)
    return response


@router.delete("/workouts/{object_id}/",
               response_model=ClimbingExerciseOut,
               response_model_exclude_none=True,
               response_model_exclude_unset=True,
               response_model_exclude_defaults=True,
               status_code=status.HTTP_200_OK)
async def delete_a_climbing_exercise_in_a_workout(object_id, current_user: dict = Depends(security.get_current_user)):
    """ Delete the exercise referenced by the object_id """

    response_status = await nosql.workouts_collection.find_one_and_delete({"_id": ObjectId(object_id),
                                                                           "username": current_user['username']})

    if response_status is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to delete exercise '{}': _id not found.".format(object_id),
                            headers={"WWW-Authenticate": "Bearer"})

    return {"exercise: {} deleted.".format(response_status)}
