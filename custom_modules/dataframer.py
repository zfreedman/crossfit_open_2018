"""
The below code is responsible for implementing information retrieval
from a MySQL database into a Pandas DataFrame using PyMySQL/Pandas
for the 2018 CrossFit Open.
"""

#import sys
import pymysql as pms
import pandas as pd

def grab_data(sql, creds):
    """
    :param sql: SQL query string
    :param creds: database credentials [host, user, pass, databasename]
    :return: 
    1. Open a connection to MySQL using PyMySQL
    2. Grab data based on the specified SQL query and store it in a Pandas dataframe
    3. Close the PyMySQL connection
    4. Return the Pandas dataframe
    """
    try:
        #connect
        con = pms.connect(host=creds[0], user=creds[1], passwd=creds[2], db=creds[3])
        
        #execute query and read into dataframe
        #(https://stackoverflow.com/questions/12047193/how-to-convert-sql-query-result-to-pandas-data-structure?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)
        df = pd.read_sql(sql, con)
    except:
        print("dataframer ERROR dataframer ERROR")
    finally:
        if con:
            #close connection
            con.close()
    
    #return dataframe
    return df

def grab_top_n_summarizer_data(n, div_id, func_str, dataframe, creds):
    """
    :param n: Top n athletes
    :param div_id: ID for the athlete division
    :param func_str: function to apply to data (MAX, MIN, AVG)
    :param dataframe: dataframe to use for column references and athlete IDs
    :param creds: database credentials (see grab_data)
    :return: dataframe (see description)
    Returns a dataframe created from the following query string:
        "SELECT {} FROM athlete WHERE division_id={} AND id IN ({});",
    or more specifically,
        "SELECT func_str(feat1), MIN(feat2), ... FROM athlete WHERE
            division_id=div_id AND id IN (id1, id2, ...);".
    This function requires the athlete ID column ('id') as a feature in the
    dataframe in addition to at least 1 field ending in reps, secs, or lbs.
    """
    return grab_data(
        """
            SELECT {} FROM athlete WHERE division_id={} AND id IN ({})
        """
        .format(
            ", ".join(
                    [
                        "{}({}) as '{}top{} {}'".format(
                        #"{}({}) as {}".format(
                            func_str, c, func_str, n,
                            #func_str, c, c
                            c.replace("leaderboard_", "")
                        )
                        for c in dataframe.columns
                           if c.endswith("reps") or c.endswith("secs") or c.endswith("lbs")
                    ]
            ),
            div_id,
            ", ".join([str(x) for x in list(dataframe.head(n)["id"])])
        ),
        creds
    )