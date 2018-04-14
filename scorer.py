"""
The below code is responsible for implementing a scoring function
for the 2018 CrossFit Open leaderboard.
"""

import sys
import pymysql as pms

def leaderboard(division, region, metric_keys, limit, creds):
    """
    :param division: int id referencing a division
    :param region: int id referencing a region
    :parm metric_keys: list of strings referencing performance metrics
    :param limit: int which limits the number of results returned
    :param creds: pymysql database connection credentials used to
        establish, query with, and close a database connection
    :return: complicated bullshit that can be read into a pandas
        dataframe

    This function will return a leaderboard scoring, ranking athletes
    from highest to lowest-performing, based on the division, region,
    and metrics specified. The division and region should be integer
    IDs referencing values from the MySQL database. The metric_keys
    should be a list ONLY containing column names in the athlete table
    which reference performance results, which include workouts/lifts
    measured in time, reps, or weight (example:
    ["back_squat_lbs", "fran_time_secs"]).

    The limit parameter will limit the returned leaderboard to the top
    *limit* athletes.

    Leaderboard ranking is done on a per-metric basis. In the mentioned
    example with metric_keys=["back_squat_lbs", "fran_time_secs"],
    athletes will first be ranked on their back squats, where the
    heaviest squat will be given rank 1, 2nd heaviest rank 2, and so on.
    Then, Fran workout times will be evaluated, where faster is better.
    The fastest Fran athlete is awarded rank 1 for Fran, 2nd fastest
    rank 2, and so on.

    Once ranking for each metric is done, the ranks for all metrics are
    for each athlete are summed together. The athlete with the smallest
    sum is ranked overall as 1st (best), second smallest is scored 2nd
    best, and so on. This sum of each rank
    (rank(back squat) + rank(fran time)) is the athlete's score, and
    it's the only metric which is used in comparing athletes for the
    overall leaderboard.

    It's important to note that ties are most likely not handled the same
    way CrossFit does (almost guaranteed). Here, 2 athletes with the same
    score will be sorted based on the underlying sorting function in this
    Python environment.

    Special cases:
    - specifying region=0 will give worldwide results (not region-specific)
    - any metric_key item which is not useful for scoring will still be
        retrieved, but not used for scoring
    """
    try:
        #connect
        con = pms.connect(host=creds[0], user=creds[1], passwd=creds[2],
            db=creds[3], charset=creds[4])

    except Exception as e:
        #output errors (if any)
        print(e)

    finally:
        #close connection
        if con:
            con.close()
    return 1
