"""
The below code is responsible for splitting list-like data into
normal/abnormal lists.
"""

import numpy as np

def separate_outliers(std_lim, vals):
    """
    :param std_lim: number of standarad deviations to limit around the mean for "normal" data
        (exclusive interval)
    :param vals: list-like values to separate
    :return: a tuple of lists of the data as (normal, outlier-like)
    """
    mean = np.mean(vals)
    std = np.std(vals)
    normal = []
    abnormal = []
    for i in vals:
        normal.append(i) if np.abs(mean - i) < std_lim * std else abnormal.append(i)
    return (normal, abnormal)