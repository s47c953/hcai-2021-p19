

def mostOfAggregation(values: [], m, n):
    result = 0.0
    for value in values:
        if value >= n:
            result += 1
        elif value <= m:
            result += 0
        else:
            result += (value - m)/(n-m)
    return result/len(values)


def conjunction(values: [], m, n):
    return min(values)


def disjunction(values: [], m, n):
    return max(values)
