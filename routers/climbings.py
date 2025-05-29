import datetime

from bson import ObjectId
from fastapi import Depends, HTTPException, APIRouter
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult
from starlette import status

from misc import security, nosql
from misc.security import oauth2_scheme
from models.climbings import ClimbingExerciseOut, ClimbingExerciseIn, ClimbingExerciseOnDB, \
    ClimbingExerciseInUpdate

router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.post('/climbings/{year}/{month}/{day}/{hour}/{minute}/{second}',
             response_model=ClimbingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED,
             tags=["climbing"])
async def add_a_climbing_exercise_to_a_workout_using_a_date(climbing_exercise: ClimbingExerciseIn,
                                                            year: int, month: int, day: int, hour: int, minute: int,
                                                            second: int,
                                                            current_user: dict = Depends(security.get_current_user)):
    """ Add a climbing exercise to the year, month, day, hour, minute and second workout. """

    when = datetime.datetime(year, month, day, hour, minute, second)

    load = compute_climbing_grade_to_load(climbing_exercise)

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
    try:

        response: InsertOneResult = await nosql.climbings_collection.insert_one(climbing_exercise_out_on_db_dict)

    except DuplicateKeyError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Unable to insert the submitted climbing exercise: "
                                   "another one exist with date {}.".format(
                                       err.details['keyValue']['when'].strftime("%Y-%m-%d %H:%M:%S")))

    climbing_exercise_out_on_db_dict['climb_id'] = response.inserted_id

    return climbing_exercise_out_on_db_dict


@router.patch("/climbings/{climb_id}",
              response_model=ClimbingExerciseOut,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK,
              tags=["climbing"])
async def update_a_climbing_exercise_in_a_workout(climbing_exercise: ClimbingExerciseInUpdate, climb_id,
                                                  current_user: dict = Depends(security.get_current_user)):
    """ Update and return an exercise referenced by the object_id """

    response = await nosql.climbings_collection.find_one(
        {"_id": ObjectId(climb_id), "username": current_user['username']})

    if climbing_exercise.grade != response['grade']:
        grade = climbing_exercise.grade
    else:
        grade = response['grade']

    load = compute_climbing_grade_to_load(climbing_exercise)

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

    _ = await nosql.climbings_collection.replace_one({"_id": ObjectId(climb_id),
                                                      "username": current_user['username']},
                                                     ceo.dict(exclude_none=True, exclude_unset=True,
                                                              exclude_defaults=True))
    ceo_dict = ceo.model_dump()
    ceo_dict['climb_id'] = climb_id

    return ceo_dict


@router.delete("/climbings/{climb_id}",
               response_model=ClimbingExerciseOut,
               response_model_exclude_none=True,
               response_model_exclude_unset=True,
               response_model_exclude_defaults=True,
               status_code=status.HTTP_200_OK,
               tags=["climbing"])
async def delete_a_climbing_exercise_in_a_workout(climb_id, current_user: dict = Depends(security.get_current_user)):
    """ Delete the exercise referenced by the object_id """

    response_status = await nosql.climbings_collection.find_one_and_delete({"_id": ObjectId(climb_id),
                                                                            "username": current_user['username']})
    if response_status is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to delete exercise '{}': _id not found.".format(climb_id),
                            headers={"WWW-Authenticate": "Bearer"})
    response_status['climb_id'] = climb_id
    return response_status


# TODO create a get climbing exercises.
def compute_climbing_grade_to_load(climbing_exercise: ClimbingExerciseIn):
    """ Compute the estimated load based on the grade climbed, total number of moves, and moves done. """
    loads = {'4a': 4, '4a+': 4.15, '4b': 4.3, '4b+': 4.45, '4c': 4.6, '4c+': 4.75,
             '5a': 5, '5a+': 5.15, '5b': 5.3, '5b+': 5.45, '5c': 5.6, '5c+': 5.75,
             '6a': 6, '6a+': 6.15, '6b': 6.3, '6b+': 6.45, '6c': 6.6, '6c+': 6.75,
             '7a': 7, '7a+': 7.15, '7b': 7.3, '7b+': 7.45, '7c': 7.6, '7c+': 7.75,
             '8a': 8, '8a+': 8.15, '8b': 8.3, '8b+': 8.45, '8c': 8.6, '8c+': 8.75,
             '9a': 9, '9a+': 9.15, '9b': 9.3, '9b+': 9.45, '9c': 9.6, '9c+': 9.75}

    # TODO: create custom validator on the class, instead of raising an exception
    if climbing_exercise.sent is True and climbing_exercise.moves:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="If sent is 'true', no moves value must be inserted")

    if climbing_exercise.sent is True:
        return loads[climbing_exercise.grade]

    # TODO: create custom validator on the class, instead of raising an exception
    if climbing_exercise.total_moves is None or climbing_exercise.moves is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="When you did not sent the problem/route, you must  insert 'moves' and total 'moves'"
                                   "to correctly calculate the load")

    # TODO: create custom validator on the class, instead of raising an exception
    if climbing_exercise.moves > climbing_exercise.total_moves:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Moves done cannot be grater than total moves on the problem/route.")

    load = (loads[climbing_exercise.grade] / int(climbing_exercise.total_moves)) * int(climbing_exercise.moves)
    return round(load, 2)
