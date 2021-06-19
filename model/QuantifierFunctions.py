
def most_of_aggregation(values: [], m, n):
    """ The most_of aggregation.
    Takes the values and returns the result depending on how many of the values fulfill the requirements of m and n.

    :param values: The values of each key which was selected. Per datapoint.
    :param m: The value for m.
    :param n: The value for n.
    :return: The aggregation result.
    """
    result = 0.0
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
    """ The conjunction aggregation.

    :param values: The values of each key which was selected. Per datapoint.
    :param m: Unused.
    :param n: Unused.
    :return: The aggregation result.
    """
    return min(values)


def disjunction(values: [], m, n):
    """ The disjunction aggregation.

    :param values: The values of each key which was selected. Per datapoint.
    :param m: Unused.
    :param n: Unused.
    :return: The aggregation result.
    """
    return max(values)
