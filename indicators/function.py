
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

