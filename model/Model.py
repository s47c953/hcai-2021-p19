from model.QuantifierFunctions import mostOfAggregation, conjunction, disjunction
from model.AggregationFunction import AggregationFunction

class Model:

    def __init__(self):
        pass

    def normalizeInputData(self, data: [{}], bounds: {}) -> [{}]:
        result = []
        for row in data:
            row_result = {}
            for key, value in row.items():
                if key == "value":
                    row_result[key] = value
                    continue

                if isinstance(value, str):
                    row_result[key] = value
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

    def ApplyQuantifierFunction(self, data: [], x_keys: [], y_keys: [], x_mode, y_mode, m=None, n=None):
        if x_mode == "mostof":
            x_function = mostOfAggregation
        elif x_mode == "conjunction":
            x_function = conjunction
        elif x_mode == "disjunction":
            x_function = disjunction
        else:
            raise Exception("Invalid data aggregation for x")

        if y_mode == "mostof":
            y_function = mostOfAggregation
        elif y_mode == "conjunction":
            y_function = conjunction
        elif y_mode == "disjunction":
            y_function = disjunction
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
            y_result = y_function(y_row, m, n)

            results.append({"x": x_result, "y": y_result})

        return results

    def restoreTargetValues(self, data, target_values) -> list:
        for key, value in target_values.items():
            data[key]["value"] = value
        return data

    def getAggregationFunctionFromString(self, target: str):
        return AggregationFunction.getClassFromString(target)

    def preparePlotTargets(self, data: list, aggregation_function, l: float, r: float) -> (list, float):
        plot_targets = []
        value_sum = 0.0
        for val in data:
            target_x = val["x"]
            target_y = val["y"]
            is_training_point = "value" in val

            # get value from aggregation function
            point_value = aggregation_function.perform(target_x, target_y, l, r)

            # add to sum
            value_sum += point_value

            # add blue color to maybe points
            if point_value != 0 and point_value != 1:
                blue_val = "44"
            else:
                blue_val = "00"

            red_val = format(255 - int(255 * point_value), 'x')
            green_val = format(int(255 * point_value), 'x')
            if len(green_val) == 1:
                green_val = "0" + green_val
            if len(red_val) == 1:
                red_val = "0" + red_val
            color = f"#{red_val}{green_val}{blue_val}"

            plot_targets.append(
                {"x": target_x, "y": target_y, "val": point_value, "color": color, "is_training_point": is_training_point})

        return plot_targets, value_sum
