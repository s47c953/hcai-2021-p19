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
        val = ((x ** r) + (y ** r) - 0.5)
        if val < 0:
            return 0.0
        elif val ** (1 / r) > 1:
            return 1.0
        else:
            return val ** (1 / r)

    @staticmethod
    def getMarker(l: float):
        x_no = [val/100 for val in range(0, 51)]
        x_yes = [val/100 for val in range(50, 101)]

        y_yes = [((-x ** l) + (0.5 ** l) + 1)**(1/l) for x in x_yes]
        y_no = [((0.5 ** l) - (x ** l))**(1/l) for x in x_no]

        return x_yes, y_yes, x_no, y_no

    @staticmethod
    def getLambdaR(data: [], r_min: float, r_max: float, l_min: float, l_max: float, resolution: float):
        min_error = sys.float_info.max
        min_l = 1.0
        min_r = 1.0

        r = r_min
        l = l_min
        while r < r_max:
            while l < l_max:
                error = 0.0
                for point in data:
                    val = LukasiewiczAggregationFunction.perform(point['x'], point['y'], l, r)
                    target = point['sol']
                    error += abs(val-target)

                if error < min_error:
                    min_error = error
                    min_l = l
                    min_r = r
                l += resolution

            r += resolution

        return min_error, min_l, min_r


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
