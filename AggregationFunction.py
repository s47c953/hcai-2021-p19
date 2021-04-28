# abstract base
import sys


class AggregationFunction:
    @staticmethod
    def perform(x: float, y: float, l: float = 1, r: float = 1) -> float:
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
    def getMarker(l: float, r: float):
        raise NotImplementedError

    @staticmethod
    def getLambdaR(data: [], r_min: float, r_max: float, l_min: float, l_max: float, resolution: float):
        raise NotImplementedError

    @staticmethod
    def findMarkerFromFunction(l: float, r: float, x_start: float, y_start: float, start_value: float, inc: float, func, inc_x=True):
        # random init
        x = x_start
        y = y_start
        res = func(x, y, l, r)
        while res == start_value:
            if inc_x:
                x += inc
            else:
                y += inc
            res = func(x, y, l, r)
        return x, y


class LukasiewiczAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, l: float = 1, r: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return LukasiewiczAggregationFunction._noFunction(x, y, l, r)
        elif x < 0.5 or y < 0.5:
            return LukasiewiczAggregationFunction._maybeFunction(x, y, l, r)
        elif x >= 0.5 and y >= 0.5:
            return LukasiewiczAggregationFunction._yesFunction(x, y, l, r)

    @staticmethod
    def _yesFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return min(1.0, ((x ** (l*r)) + (y ** (l*r)) - (0.5 ** l))) ** (1 / (l*r))

    @staticmethod
    def _noFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return max(0.0, ((x ** (l*r)) + (y ** (l*r)) - (0.5 ** l))) ** (1 / (l*r))

    @staticmethod
    def _maybeFunction(x: float, y: float, l: float, r: float = 1) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        # todo: check that hack
        val = ((x ** (l*r)) + (y ** (l*r)) - (0.5 ** l))
        if val < 0:
            return 0.0
        elif val > 1:
            return 1.0
        else:
            return val ** (1 / (l*r))

    @staticmethod
    def getMarker(l: float, r: float) -> {}:
        upper_marker_x, upper_marker_y = AggregationFunction.findMarkerFromFunction(l, r, 1, 1, 1, -0.01,
                                                                                    LukasiewiczAggregationFunction._yesFunction,
                                                                                    True)
        lower_marker_x, lower_marker_y = AggregationFunction.findMarkerFromFunction(l, r, 0, 0, 0, 0.01,
                                                                                    LukasiewiczAggregationFunction._noFunction,
                                                                                    True)
        right_marker_x, right_marker_y = AggregationFunction.findMarkerFromFunction(l, r, 1, 1, 1, -0.01,
                                                                                    LukasiewiczAggregationFunction._yesFunction,
                                                                                    False)
        left_marker_x, left_marker_y = AggregationFunction.findMarkerFromFunction(l, r, 0, 0, 0, 0.01,
                                                                                  LukasiewiczAggregationFunction._noFunction,
                                                                                  False)

        # ux and ry have to be inverted since the result was calculated from the top right hand corner
        return {'ux': 1 - upper_marker_x, 'uy': upper_marker_y, 'lox': lower_marker_x, 'loy': lower_marker_y,
                'rx': right_marker_x, 'ry': 1 - right_marker_y, 'lx': left_marker_x, 'ly': left_marker_y}

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
        return x ** (l*r) + y ** (l*r) - 0.5 ** l


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
        return -1 + 2 * x + 2 * y - 2 * x * y

    @staticmethod
    def _noFunction(x: float, y: float, l: float, r: float = 1) -> float:
        return TnormTconormAggregationFunction._maybeFunction(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float, l: float, r: float = 1) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return 2 * x * y
