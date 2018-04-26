"""
The below code is responsible for splitting list-like data into
normal/abnormal lists.
"""

import numpy as np

def separate_outliers(std_lim, df, col):
    """
    :param std_lim: number of standarad deviations to limit around the mean for "normal" data
        (exclusive interval)
    :param df: dataframe of values to separate
    :param col: column of data to analyze
    :return: a tuple of dataframes as (normal, outlier-like)
    """
    mean = np.mean(df[col])
    std = np.std(df[col])
    normal = df[np.abs(df[col] - mean) < std_lim * std]
    abnormal = df[np.abs(df[col] - mean) >= std_lim * std]
    return (normal, abnormal)