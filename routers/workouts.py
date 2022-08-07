import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException
from pymongo.results import InsertOneResult

from misc import security, exercises_climbing, nosql
from misc.exercises_climbing import build_workout_details
from models.exercises_climbing import ClimbingExerciseIn, ClimbingExerciseInUpdate
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


@router.post("/workouts/now",
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

    climbing_exercise_out_on_db = ClimbingExerciseOnDB(grade=climbing_exercise.grade,
                                                       moves=climbing_exercise.moves,
                                                       total_moves=climbing_exercise.total_moves,
                                                       sent=climbing_exercise.sent,
                                                       load=load,
                                                       when=when,
                                                       username=current_user['username'])

    climbing_exercise_out_on_db_dict = climbing_exercise_out_on_db.dict(exclude_none=True,
                                                                        exclude_unset=True,
                                                                        exclude_defaults=True)
    response: InsertOneResult = await nosql.workouts_collection.insert_one(climbing_exercise_out_on_db_dict)

    climbing_exercise_out_on_db_dict['_id'] = response.inserted_id

    return climbing_exercise_out_on_db_dict


@router.post('/workouts/{year}/{month}/{day}/{hour}/{minute}/{second}',
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_climbing_exercise_to_workout(climbing_exercise: ClimbingExerciseIn,
                                           year, month, day, hour, minute, second,
                                           current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to the year, month, day, hour, minute and second workout. """

    when = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)

    climbing_exercise_out_on_db = ClimbingExerciseOnDB(grade=climbing_exercise.grade,
                                                       moves=climbing_exercise.moves,
                                                       total_moves=climbing_exercise.total_moves,
                                                       sent=climbing_exercise.sent,
                                                       load=load,
                                                       when=when,
                                                       username=current_user['username'])

    climbing_exercise_out_on_db_dict = climbing_exercise_out_on_db.dict(exclude_none=True,
                                                                        exclude_unset=True,
                                                                        exclude_defaults=True)

    response: InsertOneResult = await nosql.workouts_collection.insert_one(climbing_exercise_out_on_db_dict)

    climbing_exercise_out_on_db_dict['_id'] = response.inserted_id

    return climbing_exercise_out_on_db_dict


@router.patch("/workouts/{_id}/",
              response_model=ClimbingExerciseOut,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK)
async def update_a_climbing_exercise_in_a_workout(climbing_exercise: ClimbingExerciseInUpdate, _id,
                                                  current_user: dict = Depends(security.get_current_user)):
    """ Update and return an exercise referenced by the object_id """

    response = await nosql.workouts_collection.find_one({"_id": ObjectId(_id), "username": current_user['username']})

    if climbing_exercise.grade != response['grade']:
        grade = climbing_exercise.grade
    else:
        grade = response['grade']

    load = exercises_climbing.compute_climbing_exercise_load(climbing_exercise)

    if climbing_exercise.when:
        when = climbing_exercise.when
    else:
        when = response['when']

    sent = climbing_exercise.sent
    if sent:
        ceo = ClimbingExerciseOnDB(grade=grade, sent=sent, load=load, when=when,
                                   username=current_user['username'])
    else:
        moves = climbing_exercise.moves
        total_moves = climbing_exercise.total_moves

        ceo = ClimbingExerciseOnDB(grade=grade, sent=sent, moves=moves, total_moves=total_moves, load=load, when=when,
                                   username=current_user['username'])

    from pprint import pprint
    pprint(ceo.dict())

    update = await nosql.workouts_collection.update_one({"_id": ObjectId(_id),
                                                         "username": current_user['username']},
                                                        {"$set": ceo.dict()})
    ceo_dict = ceo.dict()
    ceo_dict['_id'] = _id

    return ceo_dict


@router.delete("/workouts/{_id}/",
               response_model=ClimbingExerciseOut,
               response_model_exclude_none=True,
               response_model_exclude_unset=True,
               response_model_exclude_defaults=True,
               status_code=status.HTTP_200_OK)
async def delete_a_climbing_exercise_in_a_workout(_id, current_user: dict = Depends(security.get_current_user)):
    """ Delete the exercise referenced by the object_id """

    response_status = await nosql.workouts_collection.find_one_and_delete({"_id": ObjectId(_id),
                                                                           "username": current_user['username']})
    if response_status is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to delete exercise '{}': _id not found.".format(_id),
                            headers={"WWW-Authenticate": "Bearer"})

    return response_status
