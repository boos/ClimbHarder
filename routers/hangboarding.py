from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult
from starlette import status

from misc import security, nosql
from misc.security import oauth2_scheme
from models.hangboarding import HangboardingExerciseOut, HangboardingExerciseIn, HangboardingExerciseOnDB, \
    HangboardingExerciseInUpdate

router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.post('/hangboarding',
             response_model=HangboardingExerciseOut,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED,
             tags=["hangboarding"])
async def add_a_hangboard_exercise_to_a_workout(hangboard_exercise: HangboardingExerciseIn,
                                                current_user: dict = Depends(security.get_current_user)):
    """ Add a hangboard exercise to a workout."""

    he_out_on_db = HangboardingExerciseOnDB(time_under_tension=hangboard_exercise.time_under_tension,
                                            expected_time_under_tension=hangboard_exercise.expected_time_under_tension,
                                            edge_size=hangboard_exercise.edge_size,
                                            grip_type=hangboard_exercise.grip_type,
                                            weight=hangboard_exercise.weight,
                                            when=hangboard_exercise.when,
                                            username=current_user['username'])

    he_out_on_db_dict = he_out_on_db.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)

    try:

        response: InsertOneResult = await nosql.hangboarding_collection.insert_one(he_out_on_db_dict)

    except DuplicateKeyError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Unable to insert the submitted hangboard exercise: "
                                   "another one exist with date {}.".format(
                                       err.details['keyValue']['when'].strftime("%Y-%m-%d %H:%M:%S")))

    he_out_on_db_dict['hang_id'] = response.inserted_id

    return he_out_on_db_dict


@router.patch("/hangboarding/{hang_id}",
              response_model=HangboardingExerciseOut,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK,
              tags=["hangboarding"])
async def patch_a_hangboard_exercise_in_a_workout(hang_id,
                                                  hangboard_exercise: HangboardingExerciseInUpdate,
                                                  current_user: dict = Depends(security.get_current_user)):
    response = await nosql.hangboarding_collection.find_one({"_id": ObjectId(hang_id),
                                                             "username": current_user['username']})

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unable to patch the hangboard exercise: {}, exercise not found.".format(hang_id))

    if hangboard_exercise.time_under_tension is not None:
        time_under_tension = hangboard_exercise.time_under_tension
    else:
        time_under_tension = response['time_under_tension']

    if hangboard_exercise.expected_time_under_tension is not None:
        expected_time_under_tension = hangboard_exercise.expected_time_under_tension
    else:
        expected_time_under_tension = response['expected_time_under_tension']

    if hangboard_exercise.when is not None:
        when = hangboard_exercise.when
    else:
        when = response['when']

    if hangboard_exercise.weight is not None:
        weight = hangboard_exercise.weight
    else:
        weight = response['weight']

    if hangboard_exercise.grip_type is not None:
        grip_type = hangboard_exercise.grip_type
    else:
        grip_type = response['grip_type']

    if hangboard_exercise.edge_size is not None:
        edge_size = hangboard_exercise.edge_size
    else:
        edge_size = response['edge_size']

    patched_hangboard_exercise = HangboardingExerciseOnDB(time_under_tension=time_under_tension,
                                                          expected_time_under_tension=expected_time_under_tension,
                                                          edge_size=edge_size,
                                                          grip_type=grip_type,
                                                          weight=weight,
                                                          when=when, username=current_user['username'])

    _ = await nosql.hangboarding_collection.update_one({"_id": ObjectId(hang_id),
                                                            "username": current_user['username']},
                                                            {"$set": patched_hangboard_exercise.dict()})
    patched_hangboard_exercise_d = patched_hangboard_exercise.dict()
    patched_hangboard_exercise_d['hang_id'] = hang_id

    return patched_hangboard_exercise_d


@router.delete("/hangboarding/{hang_id}",
               response_model=HangboardingExerciseOut,
               response_model_exclude_none=True,
               response_model_exclude_unset=True,
               response_model_exclude_defaults=True,
               status_code=status.HTTP_200_OK,
               tags=["hangboarding"])
async def delete_a_hangboard_exercise_in_a_workout(hang_id, current_user: dict = Depends(security.get_current_user)):

    response_status = await nosql.hangboarding_collection.find_one_and_delete({"_id": ObjectId(hang_id),
                                                                               "username": current_user['username']})
    if response_status is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unable to delete the hangboard exercide '{}': hang_id not found.".format(id),
                            headers={"WWW-Authenticate": "Bearer"})

    response_status['hang_id'] = hang_id

    return response_status
