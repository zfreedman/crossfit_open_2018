"""
The below code is responsible for implementing a scoring function
for the 2018 CrossFit Open leaderboard.
"""

import sys
import pymysql as pms

def leaderboard(division, region, limit, column_keys, creds):
    """
    :param division: int id referencing a division
    :param region: int id referencing a region
    :param limit: int which limits the number of results returned
    :parm column_keys: list of strings referencing performance metrics
        and other non-scoring database columns in the athlete table
        (id should be one of them)
    :param creds: pymysql database connection credentials used to
        establish, query with, and close a database connection
    :return: complicated bullshit that can be read into a pandas
        dataframe

    This function will return a leaderboard scoring, ranking athletes
    from highest to lowest-performing, based on the division, region,
    and columns specified. The division and region should be integer
    IDs referencing values from the MySQL database. The column_keys
    should be a list containing column names in the athlete table,
    some of which should reference performance results, including
    workouts/lifts measured in time, reps, or weight (example:
    ["id", "back_squat_lbs", "fran_time_secs"]).

    The limit parameter will limit the returned leaderboard to the top
    *limit* athletes.

    Leaderboard ranking is done on a per-metric basis. In the mentioned
    example with column_keys=["id", "back_squat_lbs", "fran_time_secs"],
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

        #filter columns used for scoring
        metrics = [c for c in column_keys if
            c.endswith("secs") or
            c.endswith("lbs") or
            c.endswith("reps") or
            c.endswith("ups")]

        #query
        result = 2
        with con.cursor() as cur:
            sql = (
                """
                    SELECT id, {} FROM athlete WHERE
                    division_id={}
                    {}
                    LIMIT {}
                """
                .format(
                    ", ".join(metrics),
                    division,
                    "" if region == 0 else "AND \nregion_id={}".format(region),
                    limit
                )
            )
            #print(sql)
            cur.execute(sql)
            result = cur.fetchall()

    except Exception as e:
        #output errors (if any)
        print(e)

    finally:
        #close connection
        if con:
            con.close()

    #return result
    return result if result else None
