from model.QuantifierFunctions import most_of_aggregation, conjunction, disjunction
from model.AggregationFunction import AggregationFunction


class Model:
    """Model Class
    The model of the MVC application.
    """

    def __init__(self):
        """ Empty Constructor """
        pass

    @staticmethod
    def normalize_input_data(data: [{}], bounds: {}) -> [{}]:
        """ Normalizes the data between 0 and 1.

        :param data: The original data.
        :param bounds: The bounds of the data. Per entry.
        :return: The normalized data.
        """
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

    @staticmethod
    def apply_quantifier_function(data: [], x_keys: [], y_keys: [], x_mode, y_mode, m=None, n=None):
        """ Calculates the x and y values for each datapoint according to the parameters set in the
        quantifier/query window.The values for m and n are only relevant for the most_of quantifier.

        :param data: The data.
        :param x_keys: The set x keys from the quantifier/query window.
        :param y_keys: The set y keys from the quantifier/query window.
        :param x_mode: The set quantifier for the x axis.
        :param y_mode: The set quantifier for the x axis.
        :param m: The value for m. Only needed for the most_of quantifier.
        :param n: The value for n. Only needed for the most_of quantifier.
        :return: The quantified data calculated by using the needed quantifier functions.
        """
        if not data:
            return []

        if x_mode == "most_of":
            x_function = most_of_aggregation
        elif x_mode == "conjunction":
            x_function = conjunction
        elif x_mode == "disjunction":
            x_function = disjunction
        else:
            raise Exception("Invalid data aggregation for x")

        if y_mode == "most_of":
            y_function = most_of_aggregation
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

    @staticmethod
    def restore_target_values(data, target_values, medical_dataset=None) -> list:
        """ Restores the target values of all data entries.
        This is to reset the target value which might have been modified by the user.
        Only applies if target values are given within the dataset.

        :param data: The quantified data.
        :param target_values: The target values extracted from the dataset.
        :return: The quantified data with the original target values.
        """
        if medical_dataset:
            for key, value in enumerate(medical_dataset):
                # data[key]["value"] = value
                if medical_dataset[key]["num"] > 0:
                    data[key]["value"] = 1
                else:
                    data[key]["value"] = 0
        else:
            for key, value in target_values.items():
                data[key]["value"] = value

        return data

    @staticmethod
    def get_aggregation_function_from_string(target: str):
        """ Returns the corresponding aggregation function by a string identifier.

        :param target: The string identifier for the aggregation function.
        :return: The aggregation function.
        """
        return AggregationFunction.get_class_from_string(target)

    @staticmethod
    def prepare_plot_targets(data: list, aggregation_function, lam_yes: float, lam_no: float, r: float) -> (list, float):
        """ Prepares the plot data for plotting. Here the values for x, y and the value of the point
        are set and the color is assigned according to the value of the datapoint.

        :param data: The quantified data.
        :param aggregation_function: The aggregation function to use.
        :param lam: the value for lambda.
        :param r: The value for r.
        :return: The plottable data and the sum of all the datapoint values.
        """
        plot_targets = []
        value_sum = 0.0
        for val in data:
            target_x = val["x"]
            target_y = val["y"]
            is_training_point = "value" in val

            # get value from aggregation function
            point_value = aggregation_function.perform(target_x, target_y, lam_yes, lam_no, r)

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
                {"x": target_x, "y": target_y, "val": point_value,
                 "color": color, "is_training_point": is_training_point}
            )

        return plot_targets, value_sum
