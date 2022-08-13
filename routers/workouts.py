import datetime

from fastapi import APIRouter, Depends, status
from pymongo.results import InsertOneResult

from misc import security, exercises_climbing, nosql
from misc.exercises_climbing import build_workout_details
from models.exercises_climbing import ClimbingExerciseIn
from models.exercises_climbing import ClimbingExerciseOut, ClimbingExerciseOnDB

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])


@router.get("/workouts/", status_code=status.HTTP_200_OK)
async def get_workout_details(current_user: dict = Depends(security.get_current_user)):
    """ Return all workouts details. """

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


@router.get("/workouts/{year}", status_code=status.HTTP_200_OK)
async def get_workout_details(year,
                              current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month. """

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises


@router.get("/workouts/{year}/{month}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month,
                              current_user: dict = Depends(security.get_current_user)):
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
async def get_workout_details(year, month, day,
                              current_user: dict = Depends(security.get_current_user)):
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
async def get_workout_details(year, month, day, hour,
                              current_user: dict = Depends(security.get_current_user)):
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
async def get_workout_details(year, month, day, hour, minute,
                              current_user: dict = Depends(security.get_current_user)):
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


@router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}/{second}", status_code=status.HTTP_200_OK)
async def get_workout_details(year, month, day, hour, minute, second,
                              current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour, minute and second """

    when = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1,
                                                                         'year': {'$year': '$when'},
                                                                         'month': {'$month': '$when'},
                                                                         'day': {'$dayOfMonth': '$when'},
                                                                         'hour': {'$hour': '$when'},
                                                                         'minute': {'$minute': '$when'},
                                                                         'second': {'$second': '$when'}}},
                                                           {'$match': {'year': {'$eq': int(year)},
                                                                       'month': {'$eq': int(month)},
                                                                       'day': {'$eq': int(day)},
                                                                       'hour': {'$eq': int(hour)},
                                                                       'minute': {'$eq': int(minute)},
                                                                       'second': {'$eq': int(minute)}}},
                                                           {'$sort': {'when': 1}}])

    exercises = await build_workout_details(response_cursor)

    return exercises
