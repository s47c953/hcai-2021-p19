

def mostOfAggregation(values: [], m, n):
    result = 0.0
    # for value in values:
    #     if value >= n:
    #         result += 1
    #     elif value <= m:
    #         result += 0
    #     else:
    #         result += (value - m)/(n-m)
    # return result/len(values)
    for value in values:
        result += value
    result /= len(values)
    if result >= n:
        return 1.0
    elif result <= m:
        return 0.0
    else:
        return (result - m)/(n-m)


def conjunction(values: [], m, n):
    return min(values)


def disjunction(values: [], m, n):
    return max(values)
