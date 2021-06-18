# abstract base
import sys
import decimal
import statistics


class AggregationFunction:

    @staticmethod
    def perform(x: float, y: float, lam: float, r: float) -> float:
        raise NotImplementedError

    @staticmethod
    def get_class_from_string(s: str):
        if s == "Lukasiewicz":
            return LukasiewiczAggregationFunction
        elif s == "MinMax":
            return MinMaxAggregationFunction
        elif s == "TnormTconormGeometric":
            return TnormTconormAggregationFunction
        elif s == "TnormTconormArithmetic":
            return TnormTconormArithmeticAggregationFunction

    @staticmethod
    def get_marker(lam: float):
        raise NotImplementedError

    @staticmethod
    def get_lambda_r(data: [], r_min: float, r_max: float, l_min: float, l_max: float, resolution: float):
        maybe_points = []
        yes_points = []
        no_points = []

        for point in data:
            if 'value' in point:
                if point['x'] <= 0.5 and point['y'] <= 0.5:
                    no_points.append(point)
                elif point['x'] <= 0.5 or point['y'] <= 0.5:
                    maybe_points.append(point)
                elif point['x'] >= 0.5 and point['y'] >= 0.5:
                    yes_points.append(point)

        r = r_min
        r_result = r
        r_error = sys.float_info.max
        r_mean_error = 0
        while r <= r_max:
            error = 0.0
            for point in maybe_points:
                value = LukasiewiczAggregationFunction._maybe_function(point['x'], point['y'], 1, r)
                target_value = point['value']
                error += abs(value - target_value)
            if error < r_error:
                r_result = r
                r_error = error
            r += resolution
        if len(maybe_points) != 0:
            r_mean_error = r_error / len(maybe_points)
        else:
            r_result = 1.0

        lam = l_min
        l_result = lam
        l_error = sys.float_info.max
        l_mean_error = 0
        while lam <= l_max:
            error = 0.0
            for point in yes_points:
                value = LukasiewiczAggregationFunction._yes_function(point['x'], point['y'], lam, 1)
                target_value = point['value']
                error += abs(value - target_value)
            for point in no_points:
                value = LukasiewiczAggregationFunction._no_function(point['x'], point['y'], lam, 1)
                target_value = point['value']
                error += abs(value - target_value)
            if error < l_error:
                l_result = lam
                l_error = error
            lam += resolution
        if len(yes_points) + len(no_points) != 0:
            l_mean_error = l_error / (len(yes_points) + len(no_points))
        else:
            l_result = 1.0

        return l_mean_error, r_mean_error, l_result, r_result


class LukasiewiczAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, lam: float, r: float) -> float:
        if x <= 0.5 and y <= 0.5:
            return LukasiewiczAggregationFunction._no_function(x, y, lam, r)
        elif x <= 0.5 or y <= 0.5:
            return LukasiewiczAggregationFunction._maybe_function(x, y, lam, r)
        elif x >= 0.5 and y >= 0.5:
            return LukasiewiczAggregationFunction._yes_function(x, y, lam, r)

    @staticmethod
    def _yes_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return min(1.0, ((x ** lam) + (y ** lam) - (0.5 ** lam))) ** (1 / lam)

    @staticmethod
    def _no_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return max(0.0, ((x ** lam) + (y ** lam) - (0.5 ** lam))) ** (1 / lam)

    @staticmethod
    def _maybe_function(x: float, y: float, lam: float, r: float = 1) -> float:
        if r == 0:
            # r = 0 means we use the geometric mean
            return (x*y) ** (1/2)
        elif r < 0:
            # r < 0 means we handle cases where x or y are 0
            if x == 0 or y == 0:
                return 0
            else:
                value = ((0.5*(x**r)) + (0.5*(y**r)))**(1/r)

        else:
            value = ((0.5*(x**r)) + (0.5*(y**r)))**(1/r)

        return statistics.median([0, 1, value])

    @staticmethod
    def get_marker(lam: float):
        x_no = [val/100 for val in range(0, 51)]
        x_yes = [val/100 for val in range(50, 101)]

        y_yes = [((-x ** lam) + (0.5 ** lam) + 1) ** (1 / lam) for x in x_yes]
        y_no = [((0.5 ** lam) - (x ** lam)) ** (1 / lam) for x in x_no]

        return x_yes, y_yes, x_no, y_no


class MinMaxAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, lam: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return MinMaxAggregationFunction._no_function(x, y, lam, r)
        elif x < 0.5 or y < 0.5:
            return MinMaxAggregationFunction._maybe_function(x, y, lam, r)
        elif x >= 0.5 and y >= 0.5:
            return MinMaxAggregationFunction._yes_function(x, y, lam, r)

    @staticmethod
    def _yes_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return max(x, y)

    @staticmethod
    def _no_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return min(x, y)

    @staticmethod
    def _maybe_function(x: float, y: float, lam: float, r: float = 1) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return x + y - 0.5

    @staticmethod
    def get_marker(lam: float):
        x_no = [0.0, 0.0, 0.5]
        y_no = [0.5, 0.0, 0.0]
        x_yes = [0.5, 1.0, 1.0]
        y_yes = [1.0, 1.0, 0.5]

        return x_yes, y_yes, x_no, y_no


class TnormTconormAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, lam: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return TnormTconormAggregationFunction._no_function(x, y, lam, r)
        elif x < 0.5 or y < 0.5:
            return TnormTconormAggregationFunction._maybe_function(x, y, lam, r)
        elif x >= 0.5 and y >= 0.5:
            return TnormTconormAggregationFunction._yes_function(x, y, lam, r)

    @staticmethod
    def _yes_function(x: float, y: float, lam: float, r: float = 1) -> float:
        x = decimal.Decimal(x)
        y = decimal.Decimal(y)
        return (-1 + (2 * x) + (2 * y) - (2 * x * y)).__float__()

    @staticmethod
    def _no_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return TnormTconormAggregationFunction._maybe_function(x, y, lam)

    @staticmethod
    def _maybe_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return 2 * x * y

    @staticmethod
    def get_marker(lam: float):
        x_no = [0.0, 0.0, 1.0]
        y_no = [1.0, 0.0, 0.0]
        x_yes = [0.5, 1.0, 1.0]
        y_yes = [1.0, 1.0, 0.5]

        return x_yes, y_yes, x_no, y_no


class TnormTconormArithmeticAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, lam: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return TnormTconormArithmeticAggregationFunction._no_function(x, y, lam, r)
        elif x < 0.5 or y < 0.5:
            return TnormTconormArithmeticAggregationFunction._maybe_function(x, y, lam, r)
        elif x >= 0.5 and y >= 0.5:
            return TnormTconormArithmeticAggregationFunction._yes_function(x, y, lam, r)

    @staticmethod
    def _yes_function(x: float, y: float, lam: float, r: float = 1) -> float:
        x = decimal.Decimal(x)
        y = decimal.Decimal(y)
        return (-1 + (2 * x) + (2 * y) - (2 * x * y)).__float__()

    @staticmethod
    def _no_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return 2 * x * y

    @staticmethod
    def _maybe_function(x: float, y: float, lam: float, r: float = 1) -> float:
        return x + y - 0.5

    @staticmethod
    def get_marker(lam: float):
        x_no = [0.0, 0.0, 0.5]
        y_no = [0.5, 0.0, 0.0]
        x_yes = [0.5, 1.0, 1.0]
        y_yes = [1.0, 1.0, 0.5]

        return x_yes, y_yes, x_no, y_no
