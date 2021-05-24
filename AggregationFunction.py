# abstract base
import sys
import decimal


class AggregationFunction:

    @staticmethod
    def perform(x: float, y: float, l: float, r: float) -> float:
        raise NotImplementedError

    @staticmethod
    def getClassFromString(s: str):
        if s == "Lukasiewicz":
            return LukasiewiczAggregationFunction
        elif s == "MinMax":
            return MinMaxAggregationFunction
        elif s == "TnormTconorm":
            return TnormTconormAggregationFunction

    @staticmethod
    def getMarker(l: float):
        raise NotImplementedError

    @staticmethod
    def getLambdaR(data: [], r_min: float, r_max: float, l_min: float, l_max: float, resolution: float):
        raise NotImplementedError


class LukasiewiczAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, l: float, r: float) -> float:
        if x <= 0.5 and y <= 0.5:
            return LukasiewiczAggregationFunction._noFunction(x, y, l, r)
        elif x <= 0.5 or y <= 0.5:
            return LukasiewiczAggregationFunction._maybeFunction(x, y, l, r)
        elif x >= 0.5 and y >= 0.5:
            return LukasiewiczAggregationFunction._yesFunction(x, y, l, r)

    @staticmethod
    def _yesFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return min(1.0, ((x ** l) + (y ** l) - (0.5 ** l))) ** (1 / l)

    @staticmethod
    def _noFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return max(0.0, ((x ** l) + (y ** l) - (0.5 ** l))) ** (1 / l)

    @staticmethod
    def _maybeFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return ((x ** r) + (y ** r) - (0.5 ** r)) ** (1 / r)

    @staticmethod
    def getMarker(l: float):
        x_no = [val/100 for val in range(0, 51)]
        x_yes = [val/100 for val in range(50, 101)]

        y_yes = [((-x ** l) + (0.5 ** l) + 1)**(1/l) for x in x_yes]
        y_no = [((0.5 ** l) - (x ** l))**(1/l) for x in x_no]

        return x_yes, y_yes, x_no, y_no

    @staticmethod
    def getLambdaR(data: [], r_min: float, r_max: float, l_min: float, l_max: float, resolution: float):

        maybe_points = []
        yes_points = []
        no_points = []

        for point in data:
            if 'sol' in point:
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
                value = LukasiewiczAggregationFunction._maybeFunction(point['x'], point['y'], 1, r)
                target_value = point['sol']
                error += abs(value - target_value)
            if error < r_error:
                r_result = r
                r_error = error
            r += resolution
        if len(maybe_points) != 0:
            r_mean_error = r_error / len(maybe_points)
        else:
            r_result = 1.0

        l = l_min
        l_result = l
        l_error = sys.float_info.max
        l_mean_error = 0
        while l <= l_max:
            error = 0.0
            for point in yes_points:
                value = LukasiewiczAggregationFunction._yesFunction(point['x'], point['y'], l, 1)
                target_value = point['sol']
                error += abs(value - target_value)
            for point in no_points:
                value = LukasiewiczAggregationFunction._noFunction(point['x'], point['y'], l, 1)
                target_value = point['sol']
                error += abs(value - target_value)
            if error < l_error:
                l_result = l
                l_error = error
            l += resolution
        if len(yes_points) + len(no_points) != 0:
            l_mean_error = l_error / (len(yes_points) + len(no_points))
        else:
            l_result = 1.0

        return l_mean_error, r_mean_error, l_result, r_result


class MinMaxAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, l: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return MinMaxAggregationFunction._noFunction(x, y, l, r)
        elif x < 0.5 or y < 0.5:
            return MinMaxAggregationFunction._maybeFunction(x, y, l, r)
        elif x >= 0.5 and y >= 0.5:
            return MinMaxAggregationFunction._yesFunction(x, y, l, r)

    @staticmethod
    def _yesFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return max(x, y)

    @staticmethod
    def _noFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return min(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float, l: float, r: float = 1) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return x + y - 0.5

    @staticmethod
    def getMarker(l: float):
        x_no = [val / 100 for val in range(0, 51)]
        x_yes = [val / 100 for val in range(50, 101)]

        y_yes = [1 for x in x_yes]
        y_no = [0 for x in x_no]

        return x_yes, y_yes, x_no, y_no


class TnormTconormAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, l: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return TnormTconormAggregationFunction._noFunction(x, y, l, r)
        elif x < 0.5 or y < 0.5:
            return TnormTconormAggregationFunction._maybeFunction(x, y, l, r)
        elif x >= 0.5 and y >= 0.5:
            return TnormTconormAggregationFunction._yesFunction(x, y, l, r)

    @staticmethod
    def _yesFunction(x: float, y: float, l: float, r: float = 1) -> float:
        x = decimal.Decimal(x)
        y = decimal.Decimal(y)
        return (-1 + (2 * x) + (2 * y) - (2 * x * y)).__float__()

    @staticmethod
    def _noFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return TnormTconormAggregationFunction._maybeFunction(x, y, l)

    @staticmethod
    def _maybeFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return 2 * x * y

    @staticmethod
    def getMarker(l: float):
        return [], [], [], []
