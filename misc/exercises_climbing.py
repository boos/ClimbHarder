from collections import OrderedDict, Counter

from fastapi import status, HTTPException

from models.exercises_climbing import ClimbingExerciseIn


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


async def compute_overall_workout_response(response_cursor):
    """ Build a dict summarizing all climbing exercises in order of time, plus workout stats. """

    workout_details = OrderedDict()

    workouts = 0

    # Total counters, and variables
    total_unsent_moves = 0
    total_load = 0
    total_sent = []
    total_unsent = []

    # workout counters, and variables
    workout_unsent_moves = 0
    workout_load = 0
    workout_sent = []
    workout_unsent = []

    previous_workout_date = None

    for exercise in await response_cursor.to_list(length=36500):

        # clean up not-needed projections data
        exercise.pop('username', None)
        exercise.pop('year', None)
        exercise.pop('month', None)
        exercise.pop('day', None)
        exercise.pop('hour', None)
        exercise.pop('minute', None)
        exercise.pop('second', None)

        exercise['_id'] = str(exercise['_id'])

        # New daily workout record creation
        if exercise['when'].strftime("%Y-%m-%d") not in workout_details:
            workouts += 1
            workout_details[exercise['when'].strftime("%Y-%m-%d")] = OrderedDict({'climbings': [],
                                                                                  'workout_sent_distribution': [],
                                                                                  'workout_unsent_moves_distribution': [],
                                                                                  'workout_sent': [],
                                                                                  'workout_unsent_moves': [],
                                                                                  'workout_load': 0})

            # It is a new workout, hence we can compute previous workout stats
            if previous_workout_date is not None and previous_workout_date != exercise['when'].strftime("%Y-%m-%d"):
                await compute_climbing_exercise_stats(workout_details, previous_workout_date, workout_load,
                                                      workout_sent, workout_unsent, workout_unsent_moves)

                workout_sent = []
                workout_unsent = []
                workout_unsent_moves = 0
                workout_load = 0

        # store exercise
        workout_details[exercise['when'].strftime("%Y-%m-%d")]['climbings'].append(exercise)

        # compute total load
        total_load += exercise['load']
        # compute workout load
        workout_load += exercise['load']

        # Count total and workout related sent to compute sent distributions
        if exercise['sent'] is True:
            total_sent.append(exercise['grade'])
            workout_sent.append(exercise['grade'])

        # Count total and workout related moves to compute moves distributions
        else:
            for i in range(0, exercise['moves']):
                total_unsent.append(exercise['grade'])
                workout_unsent.append(exercise['grade'])

            # count total moves
            total_unsent_moves += exercise['moves']
            # count workout moves
            workout_unsent_moves += exercise['moves']

        previous_workout_date = exercise['when'].strftime("%Y-%m-%d")

    # compute last workout
    await compute_climbing_exercise_stats(workout_details, previous_workout_date, workout_load, workout_sent,
                                          workout_unsent, workout_unsent_moves)

    # compute all workouts
    workout_details['workouts'] = workouts
    workout_details['sent_distribution'] = Counter(total_sent).most_common()
    workout_details['unsent_moves_distribution'] = Counter(total_unsent).most_common()
    workout_details['total_sent'] = len(total_sent)
    workout_details['total_unsent_moves'] = total_unsent_moves
    workout_details['total_load'] = round(total_load, 2)

    return workout_details


async def compute_climbing_exercise_stats(exercises, previous_workout_date, workout_load, workout_sent,
                                          workout_unsent, workout_unsent_moves):
    012.
    """ Compute some climbing exercise """

    exercises[previous_workout_date]['workout_sent_distribution'] = Counter(workout_sent).most_common()
    exercises[previous_workout_date]['workout_unsent_moves_distribution'] = Counter(workout_unsent).most_common()
    exercises[previous_workout_date]['workout_sent'] = len(workout_sent)
    exercises[previous_workout_date]['workout_unsent_moves'] = workout_unsent_moves
    exercises[previous_workout_date]['workout_load'] = round(workout_load, 2)
