
def highest(series_a, length):
    newList = []
    if length > len(series_a):
        return series_a[len(series_a)-1]
    else:
        for x in range(length):
            newList.append(series_a[len(series_a) - 1 - x])
        return max(newList)




def lowest(series_a, length):
    newList = []
    if length>len(series_a):
        return series_a[len(series_a)-1]
    else :
        for x in range(length):
            newList.append(series_a[len(series_a) - 1 - x])
        return min(newList)

def cross_above(series_a, series_b):
    """
    Checks the up-intersection of the first series sent to the second series or value
    :param series_a:
    :param series_b:
    :return: true or false
    """
    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    series_b = pd.Series(series_b) if isinstance(series_b, list) else series_b if isinstance(series_b,pd.Series) else pd.Series(data=[series_b,series_b])
    pre_short = series_a.iloc[-2]
    short = series_a.iloc[-1]

    pre_long = series_b.iloc[-2]
    long = series_b.iloc[-1]


    if pre_short < pre_long and short > long:
        return True
    else:
        return False
