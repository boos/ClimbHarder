from fastapi import status, HTTPException

from models.exercises_climbing import ClimbingExerciseIn


def compute_climbing_exercise_load(climbing_exercise: ClimbingExerciseIn):
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
        return loads[climbing_exercise.grade.value]

    # TODO: create custom validator on the class, instead of raising an exception
    if climbing_exercise.total_moves is None or climbing_exercise.moves is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="When you did not sent the problem/route, you must  insert 'moves' and total 'moves'"
                                   "to correctly calculate the load")

    # TODO: create custom validator on the class, instead of raising an exception
    if climbing_exercise.moves > climbing_exercise.total_moves:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Moves done cannot be grater than total moves on the problem/route.")

    load = (loads[climbing_exercise.grade.value]/climbing_exercise.total_moves)*climbing_exercise.moves
    return round(load, 2)


async def build_workout_details(response_cursor):
    """ Build a dict containing all exercises in sequence plus total work and number of exercises """

    exercises = dict()
    exercises['climbing_exercises'] = list()
    exercises['distribution_of_climbing_exercises'] = dict()
    exercises['total_load'] = 0

    for exercise in await response_cursor.to_list(length=256):

        exercise['_id'] = str(exercise['_id'])
        exercise.pop('username', None)
        exercise.pop('year', None)
        exercise.pop('month', None)
        exercise.pop('day', None)
        exercise.pop('hour', None)
        exercise.pop('minute', None)

        exercises['climbing_exercises'].append(exercise)

        if exercise['grade'] not in exercises['distribution_of_climbing_exercises']:
            exercises['distribution_of_climbing_exercises'][exercise['grade']] = dict()

        if exercise['sent']:
            if 'sent' not in exercises['distribution_of_climbing_exercises'][exercise['grade']]:
                exercises['distribution_of_climbing_exercises'][exercise['grade']]['sent'] = 1
            else:
                exercises['distribution_of_climbing_exercises'][exercise['grade']]['sent'] += 1
        else:
            if 'moves' not in exercises['distribution_of_climbing_exercises'][exercise['grade']]:
                exercises['distribution_of_climbing_exercises'][exercise['grade']]['moves'] = list()
            exercises['distribution_of_climbing_exercises'][exercise['grade']]['moves'].append((
                exercise['moves'], exercise['total_moves']))

        exercises['total_load'] = exercises['total_load'] + exercise['load']

    exercises['total_load'] = round(exercises['total_load'], 2)
    exercises['number_of_climbing_exercises'] = len(exercises['climbing_exercises'])

    return exercises
