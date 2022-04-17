import numpy as np
import pandas as pd


def highest(series_a, length):
    """
    Returns the highest element in the given series
    :param series_a:
    :param length:
    :return:
    """

    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    newList = pd.Series(dtype=series_a.dtype, index=np.arange(length))
    length = series_a.size if length > series_a.size else length
    for x in range(length):
        newList[x] = series_a.iloc[-1-x]
    return newList.max()


def lowest(series_a, length):
    """
    Returns the lowest element in the given series
    :param series_a:
    :param length:
    :return:
    """

    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    newList = pd.Series(dtype=series_a.dtype, index=np.arange(length))
    length = series_a.size if length > series_a.size else length
    for x in range(length):
        newList[x] = series_a.iloc[-1-x]
    return newList.min()



def sum(series_a, length):
    """
    Sums back by the number of elements in the given list
    :param series_a:
    :param length:
    :return:
    """
    sum = 0
    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    length = series_a.size if length > series_a.size else length
    for i in range(length):
        sum += series_a.iloc[-1 - i]
    return sum


def distance(series_a, value):
    """
    Value is searched by traversing the given series from the end
    :param series_a:
    :param value:
    :return:
    """
    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    d = 0

    for i in range(series_a.size):
        if value == series_a.iloc[- 1 - i]:
            d = i
            break
    return d


# CROSS
def cross_above(series_a, series_b):
    """
    Checks the up-intersection of the first series sent to the second series or value
    :param series_a:
    :param series_b:
    :return: true or false
    """
    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    series_b = pd.Series(series_b) if isinstance(series_b, list) else series_b if isinstance(series_b,
                                                                                             pd.Series) else pd.Series(
        data=[series_b, series_b])
    pre_short = series_a.iloc[-2]
    short = series_a.iloc[-1]

    pre_long = series_b.iloc[-2]
    long = series_b.iloc[-1]

    if pre_short < pre_long and short > long:
        return True
    else:
        return False
