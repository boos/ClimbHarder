import datetime
from collections import OrderedDict, Counter

from fastapi import APIRouter, Depends, status

from misc import security, nosql

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])


@router.get("/workouts/", status_code=status.HTTP_200_OK)
async def get_workout_details(current_user: dict = Depends(security.get_current_user)):
    """ Return all workouts details. """

    response_cursor = nosql.workouts_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                           {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                         'when': 1, 'moves': 1, 'total_moves': 1,
                                                                         '_id': 1}},
                                                           {'$sort': {'when': 1}}])

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

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

    exercises = await compute_workout_climbing_response(response_cursor)

    return exercises


async def compute_workout_climbing_response(response_cursor):
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
                await compute_workout_climbing_stats(workout_details, previous_workout_date, workout_load,
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
    await compute_workout_climbing_stats(workout_details, previous_workout_date, workout_load, workout_sent,
                                         workout_unsent, workout_unsent_moves)

    # compute all workouts
    workout_details['workouts'] = workouts
    workout_details['sent_distribution'] = Counter(total_sent).most_common()
    workout_details['unsent_moves_distribution'] = Counter(total_unsent).most_common()
    workout_details['total_sent'] = len(total_sent)
    workout_details['total_unsent_moves'] = total_unsent_moves
    workout_details['total_load'] = round(total_load, 2)

    return workout_details


async def compute_workout_climbing_stats(exercises, previous_workout_date, workout_load, workout_sent,
                                         workout_unsent, workout_unsent_moves):
    012.
    """ Compute some climbing exercise """

    exercises[previous_workout_date]['workout_sent_distribution'] = Counter(workout_sent).most_common()
    exercises[previous_workout_date]['workout_unsent_moves_distribution'] = Counter(workout_unsent).most_common()
    exercises[previous_workout_date]['workout_sent'] = len(workout_sent)
    exercises[previous_workout_date]['workout_unsent_moves'] = workout_unsent_moves
    exercises[previous_workout_date]['workout_load'] = round(workout_load, 2)
