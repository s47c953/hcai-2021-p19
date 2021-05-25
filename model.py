

def normalizeInputData(data: [{}], bounds: {}) -> [{}]:

    result = []

    for row in data:
        row_result = {}
        for key, value in row.items():
            if key == "value":
                row_result[key] = value
                break
            target_bound_min = bounds[key]["min"]
            target_bound_max = bounds[key]["max"]

            # reduce value to bounds
            if value > target_bound_max:
                temp_value = target_bound_max
            elif value < target_bound_min:
                temp_value = target_bound_min
            else:
                temp_value = value

            normalize_value = ((temp_value - target_bound_min) / (target_bound_max - target_bound_min))
            row_result[key] = normalize_value
        result.append(row_result)

    return result
