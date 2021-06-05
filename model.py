import DataAggregation

def normalizeInputData(data: [{}], bounds: {}) -> [{}]:

    result = []

    for row in data:
        row_result = {}
        for key, value in row.items():
            if key == "value":
                row_result[key] = value
                continue

            if isinstance(value, str):
                continue

            target_bound_min = bounds[key]["min"]
            target_bound_max = bounds[key]["max"]
            inverse = False

            if target_bound_max < target_bound_min:
                target_bound_max, target_bound_min = target_bound_min, target_bound_max
                inverse = True

            # reduce value to bounds
            if value > target_bound_max:
                temp_value = target_bound_max
            elif value < target_bound_min:
                temp_value = target_bound_min
            else:
                temp_value = value

            normalize_value = ((temp_value - target_bound_min) / (target_bound_max - target_bound_min))
            if inverse:
                normalize_value = 1 - normalize_value
            row_result[key] = normalize_value
        result.append(row_result)

    return result


def aggregateData(data: [], x_keys: [], y_keys: [], x_mode, y_mode, m = None, n = None):
    if x_mode == "most_of":
        x_function = DataAggregation.mostOfAggregation
    elif x_mode == "conjunction":
        x_function = DataAggregation.conjunction
    elif x_mode == "disjunction":
        x_function = DataAggregation.disjunction
    else:
        raise Exception("Invalid data aggregation for x")

    if y_mode == "most_of":
        y_function = DataAggregation.mostOfAggregation
    elif y_mode == "conjunction":
        y_function = DataAggregation.conjunction
    elif y_mode == "disjunction":
        y_function = DataAggregation.disjunction
    else:
        raise Exception("Invalid data aggregation for y")

    results = []

    for data_point in data:
        x_row = []
        y_row = []
        for x_key in x_keys:
            x_row.append(data_point[x_key])
        for y_key in y_keys:
            y_row.append(data_point[y_key])

        x_result = x_function(x_row, m, n)
        y_result = y_function(x_row, m, n)

        results.append({"x": x_result, "y": y_result})

    return results