import datetime
from collections import OrderedDict, Counter

from fastapi import APIRouter, Depends, status

from misc import security, nosql

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])


async def compute_workout_climbing_response(response_cursor):
    """ Build a dict summarizing all climbing exercises in order of time, and relative workouts stats. """

    workout_details = OrderedDict()

    workouts = 0

    # Count total number of unsent moves
    total_unsent_moves = 0
    # Store total load of sent climb
    total_sent_load = 0
    # Store total load of moves not leading to a sent
    total_unsent_moves_load = 0
    # Store the overall load of sent and unsent climbs
    total_load = 0
    total_sent = []
    total_unsent = []

    # Count number of unsent moves per workout
    workout_unsent_moves = 0
    # Store on which grades we made unsent moves attempts
    workout_unsent_climbings_grades = []
    # Count unsent moves load per workout
    workout_unsent_moves_load = 0

    # Don't count number of sent as we will use len()
    # workout_sent = 0
    # Store on which grade we sent
    workout_sent_climbings_grades = []
    # Count sent load per workout
    workout_sent_load = 0

    # Store rests time between exercises
    # Does it make sense to track the distribution?
    # workout_rests_time = []

    # Count unsent and sent overall load
    workout_total_load = 0

    previous_workout_date = None
    previous_exercise_datetime = None

    exercise = {'when': None}

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
                                                                                  'workout_sent_load': 0,
                                                                                  'workout_unsent_moves_load': 0,
                                                                                  'workout_total_load': 0})

            # It is a new workout, hence we can compute previous workout stats
            if previous_workout_date is not None and previous_workout_date != exercise['when'].strftime("%Y-%m-%d"):
                await compute_workout_climbing_stats(workout_details,
                                                     previous_workout_date, exercise['when'],
                                                     workout_sent_climbings_grades, workout_unsent_climbings_grades,
                                                     workout_unsent_moves,
                                                     workout_sent_load, workout_unsent_moves_load, workout_total_load)

                workout_sent_climbings_grades = []
                workout_unsent_climbings_grades = []
                workout_unsent_moves = 0
                workout_sent_load = 0
                workout_unsent_moves_load = 0
                workout_total_load = 0

                previous_exercise_datetime = None

        # if a previous exercise was inserted, compute rest time between this and previous exercise
        if previous_exercise_datetime is not None:
            td = exercise['when'] - previous_exercise_datetime
            hours = td.seconds // 3600
            minutes = td.seconds % 3600 // 60
            seconds = td.seconds - hours * 3600 - minutes * 60
            exercise['rest'] = "{}:{}".format(minutes, seconds)

        # store exercise
        workout_details[exercise['when'].strftime("%Y-%m-%d")]['climbings'].append(exercise)

        # compute total load
        total_load += exercise['load']
        # compute total workout load
        workout_total_load += exercise['load']

        # Store all sent and workout sent to subsequently compute workout and total sent distributions
        if exercise['sent'] is True:
            workout_sent_climbings_grades.append(exercise['grade'])
            total_sent.append(exercise['grade'])

            # we don't count total sent as we can simply use len afterwards

            # Calculate workout sent load
            workout_sent_load += exercise['load']
            # Calculate total sent load
            total_sent_load += exercise['load']

        # Store all unsent and workout moves to subsequently compute workout and total unsent moves distributions
        if exercise['sent'] is False:
            for _ in range(0, exercise['moves']):
                workout_unsent_climbings_grades.append(exercise['grade'])
                total_unsent.append(exercise['grade'])

            # count workout moves as we can't use len() as per sent
            workout_unsent_moves += exercise['moves']
            # count total moves as we can't use len() as per sent
            total_unsent_moves += exercise['moves']

            # Calculate unsent moves load
            workout_unsent_moves_load += exercise['load']
            # Calculate total unsent moves load
            total_unsent_moves_load += exercise['load']

        previous_workout_date = exercise['when'].strftime("%Y-%m-%d")
        previous_exercise_datetime = exercise['when']

    # compute workout climbing stats such as load, etc.
    await compute_workout_climbing_stats(workout_details,
                                         previous_workout_date, exercise['when'],
                                         workout_sent_climbings_grades, workout_unsent_climbings_grades,
                                         workout_unsent_moves,
                                         workout_sent_load, workout_unsent_moves_load, workout_total_load)

    # compute all workouts
    workout_details['workouts'] = workouts
    workout_details['sent_distribution'] = Counter(total_sent).most_common()
    workout_details['unsent_moves_distribution'] = Counter(total_unsent).most_common()
    workout_details['total_sent'] = len(total_sent)
    workout_details['total_unsent_moves'] = total_unsent_moves
    workout_details['total_sent_load'] = round(total_sent_load, 2)
    workout_details['total_unsent_moves_load'] = round(total_unsent_moves_load, 2)
    workout_details['total_load'] = round(total_load, 2)

    return workout_details


async def compute_workout_climbing_stats(exercises,
                                         previous_workout_date, current_workout_date,
                                         workout_climbings_grade_sent, workout_climbings_grade_unsent,
                                         workout_unsent_moves_number,
                                         workout_sent_load, workout_unsent_moves_load, workout_total_load):
    """ Compute some climbing exercise """

    if previous_workout_date is None or current_workout_date is None:
        return

    exercises[previous_workout_date]['workout_sent_distribution'] = Counter(workout_climbings_grade_sent).most_common()
    exercises[previous_workout_date]['workout_unsent_moves_distribution'] = Counter(
        workout_climbings_grade_unsent).most_common()
    exercises[previous_workout_date]['workout_#_sent'] = len(workout_climbings_grade_sent)
    exercises[previous_workout_date]['workout_#_unsent_moves'] = workout_unsent_moves_number
    exercises[previous_workout_date]['workout_sent_load'] = round(workout_sent_load, 2)
    exercises[previous_workout_date]['workout_unsent_moves_load'] = round(workout_unsent_moves_load, 2)
    exercises[previous_workout_date]['workout_total_load'] = round(workout_total_load, 2)

    previous_workout_date_dt = datetime.datetime.strptime(previous_workout_date, "%Y-%m-%d")
    if current_workout_date.date() != previous_workout_date_dt.date():

        exercises[previous_workout_date]['workout_rest_days'] = (current_workout_date - previous_workout_date_dt).days


@router.get("/workouts", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_all_workout_details(current_user: dict = Depends(security.get_current_user)):
    """ Return all workouts details. """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                            {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                          'when': 1, 'moves': 1, 'total_moves': 1,
                                                                          '_id': 1}},
                                                            {'$sort': {'when': 1}}])

    exercises = await compute_workout_climbing_response(response_cursor)

    return exercises


@router.get("/workouts/latest", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_latest_workout_details(current_user: dict = Depends(security.get_current_user)):

    # Find latest workout for the user
    response_cursor = nosql.climbings_collection.find({'username': current_user['username']}).sort('when', -1).limit(1)
    documents_list = await response_cursor.to_list(length=1)
    document = documents_list[0]

    return await get_year_month_day_workout_details(document['when'].year, document['when'].month,
                                                    document['when'].day, current_user)


@router.get("/workouts/today", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_today_workout_details(current_user: dict = Depends(security.get_current_user)):
    """ Return today workout details. """

    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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


@router.get("/workouts/{year}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_workout_details(year, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month. """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
                                                            {'$project': {'grade': 1, 'sent': 1, 'load': 1,
                                                                          'when': 1, 'moves': 1, 'total_moves': 1,
                                                                          '_id': 1,
                                                                          'year': {'$year': '$when'}}},
                                                            {'$match': {'year': {'$eq': int(year)}}},
                                                            {'$sort': {'when': 1}}])

    exercises = await compute_workout_climbing_response(response_cursor)

    return exercises


@router.get("/workouts/{year}/{month}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_month_workout_details(year, month, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month. """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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


@router.get("/workouts/{year}/{month}/{day}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_month_day_workout_details(year, month, day, current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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


@router.get("/workouts/{year}/{month}/{day}/{hour}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_month_day_hour_workout_details(year, month, day, hour,
                                                  current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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


@router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_month_day_hour_minute_workout_details(year, month, day, hour, minute,
                                                         current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour, and minute """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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


@router.get("/workouts/{year}/{month}/{day}/{hour}/{minute}/{second}", status_code=status.HTTP_200_OK, tags=["workouts"])
async def get_year_month_day_hour_minute_second_workout_details(year, month, day, hour, minute, second,
                                                                current_user: dict = Depends(security.get_current_user)):
    """ Return workout details within a specified year, month, day, hour, minute and second """

    response_cursor = nosql.climbings_collection.aggregate([{'$match': {'username': current_user["username"]}},
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
                                                                        'second': {'$eq': int(second)}}},
                                                            {'$sort': {'when': 1}}])

    exercises = await compute_workout_climbing_response(response_cursor)

    return exercises
