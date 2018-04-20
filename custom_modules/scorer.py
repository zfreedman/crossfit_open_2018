"""
The below code is responsible for implementing a scoring function
for the 2018 CrossFit Open leaderboard.
"""

import sys
import pymysql as pms
import pandas as pd
from functools import reduce

def leaderboard(division, region, column_keys, creds):
    """
    :param division: int id referencing a division
    :param region: int id referencing a region
    :param limit: int which limits the number of results returned
    :parm column_keys: list of strings referencing performance metrics
        and other non-scoring database columns in the athlete table
        (id should be one of them)
    :param creds: pymysql database connection credentials used to
        establish, query with, and close a database connection
    :return: leaderboard data as a pandas dataframe

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

    PLEASE READ:
    - any athlete with a metric value of -1 for ANY of the specified column_keys
        which could be used as metrics WILL NOT be included in the leaderboard.
        These are considered DNF (did not finish) in this codebase.
    """

    #result = None
    #sub_boards = None
    #merged_board = None
    final_board = None

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
        non_metrics = [c for c in column_keys if c not in metrics]

        #query
        #https://stackoverflow.com/questions/3126972/with-mysql-how-can-i-generate-a-column-containing-the-record-index-in-a-table?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        sql = (
            """
                SELECT {}, {}
                    FROM athlete
                    WHERE
                        division_id={}
                        {} AND
                        {};
            """
            .format(
                ", ".join(non_metrics),
                ", ".join(metrics),
                division,
                "" if region == 0 else "AND \nregion_id={}".format(region),
                " AND ".join(["{}!=-1".format(c) for c in metrics])
            )
        )
        #print(sql)

        #store result in dataframe
        result = pd.read_sql(sql, con)

        #do scoring in python
        #(could be done solely in SQL, but i don't know enough yet)

        #get leaderboards for each individual metric
        sub_boards = [result[["id", m]] for m in metrics]
        #sort as needed
        sub_boards = [
            s.sort_values(
                s.columns[-1],
                axis=0,
                ascending=True if s.columns[-1].endswith("secs") else False
            ).reset_index(drop=True) for s in sub_boards
        ]
        #concat index column (ranking by sort method)
        sub_boards = [pd.concat([s, pd.DataFrame(s.index)], axis=1)
            for s in sub_boards]
        #rename indexing column
        sub_boards = [
            s.rename(
                columns={
                    s.columns[-1]: "score {}".format(s.columns[-2])
                }
            )
            for s in sub_boards]
        #merge on athlete id
        #https://stackoverflow.com/questions/23668427/pandas-joining-multiple-dataframes-on-columns?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        merged_board = reduce(
            lambda left, right: pd.merge(left, right, on="id"),
            sub_boards
        )
        #sum scores
        merged_board = pd.concat([merged_board,
            None if len(sub_boards) == 1 else reduce(
            lambda left, right: left + right,
            [
                merged_board[c] for c in merged_board.columns
                    if c.startswith("score")
            ]
        )], axis=1)
        #rename summed column
        merged_board = merged_board.rename(
            columns={
                merged_board.columns[-1]: "points"
            }
        )
        #drop individual scoring columns
        merged_board = merged_board.drop(
            [c for c in merged_board.columns if c.startswith("score")],
            axis = 1
        )
        #get complete data board with non-metrics included
        non_metrics_board = result[non_metrics]
        final_board = pd.merge(
            non_metrics_board, merged_board, on="id"
        ).sort_values("points")

    finally:
        #close connection
        if con:
            con.close()

    #return result
    #return sub_boards
    #return merged_board
    return final_board
