import datetime

from bson import ObjectId
from fastapi import Depends, HTTPException
from pymongo.results import InsertOneResult
from starlette import status

from misc import security, exercises_climbing, nosql
from models.exercises_climbing import ClimbingExerciseOut, ClimbingExerciseIn, ClimbingExerciseOnDB, \
    ClimbingExerciseInUpdate
from routers.workouts import router


@router.post("/climbings/now",
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_a_climbing_exercise_done_now_to_a_workout(climbing_exercise: ClimbingExerciseIn,
                                                        current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to a specific workout done now """

    when = datetime.datetime.now()

    load = exercises_climbing.compute_climbing_grade_to_load(climbing_exercise)

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


@router.post('/climbings/{year}/{month}/{day}/{hour}/{minute}/{second}',
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED)
async def add_a_climbing_exercise_using_a_date_to_a_workout(climbing_exercise: ClimbingExerciseIn,
                                                            year, month, day, hour, minute, second,
                                                            current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to the year, month, day, hour, minute and second workout. """

    when = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    load = exercises_climbing.compute_climbing_grade_to_load(climbing_exercise)

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


@router.patch("/climbings/{id}/",
              response_model=ClimbingExerciseOut,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK)
async def update_a_climbing_exercise_in_a_workout(climbing_exercise: ClimbingExerciseInUpdate, object_id,
                                                  current_user: dict = Depends(security.get_current_user)):
    """ Update and return an exercise referenced by the object_id """

    response = await nosql.workouts_collection.find_one({"_id": ObjectId(object_id), "username": current_user['username']})

    if climbing_exercise.grade != response['grade']:
        grade = climbing_exercise.grade
    else:
        grade = response['grade']

    load = exercises_climbing.compute_climbing_grade_to_load(climbing_exercise)

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

    update = await nosql.workouts_collection.update_one({"_id": ObjectId(object_id),
                                                         "username": current_user['username']},
                                                        {"$set": ceo.dict()})
    ceo_dict = ceo.dict()
    ceo_dict['_id'] = object_id

    return ceo_dict


@router.delete("/climbings/{id}/",
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


# TODO create a get climbing exercises.
