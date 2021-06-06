

def preparePlotTargets(data: [dict], inverse_x: bool, inverse_y: bool, aggregation_function, l: float, r: float) -> ([dict], float):

    #TODO: apply query
    x_key = "x"
    y_key = "y"

    plot_targets = []
    value_sum = 0.0
    for val in data:
        target_x = val[x_key]
        target_y = val[y_key]
        is_training_point = "value" in val

        # inverse for plot if necessary
        if inverse_x:
            target_x = 1 - target_x
        if inverse_y:
            target_y = 1 - target_y

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

        plot_targets.append({"x": target_x, "y": target_y, "val": point_value, "color": color, "is_training_point": is_training_point})

    return plot_targets, value_sum


