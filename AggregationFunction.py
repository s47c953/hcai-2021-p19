
# abstract base
class AggregationFunction:
    @staticmethod
    def perform(x: float, y: float, k: float = 1) -> float:
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
    def getMarker(k: float):
        raise NotImplementedError

    @staticmethod
    def findMarkerFromFunction(k: float, x_start: float, y_start: float, start_value: float, inc: float,  func, inc_x = True):
        # random init
        x = x_start
        y = y_start
        res = func(x, y, k)
        while res == start_value:
            if inc_x:
                x += inc
            else:
                y += inc
            res = func(x, y, k)
        return x, y



class LukasiewiczAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, k: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return LukasiewiczAggregationFunction._noFunction(x, y, k)
        elif x < 0.5 or y < 0.5:
            return LukasiewiczAggregationFunction._maybeFunction(x, y, k)
        elif x >= 0.5 and y >= 0.5:
            return LukasiewiczAggregationFunction._yesFunction(x, y, k)

    @staticmethod
    def _yesFunction(x: float, y: float, k: float) -> float:
        return min(1.0, (x**k+y**k-0.5**k))**(1/k)

    @staticmethod
    def _noFunction(x: float, y: float, k: float) -> float:
        return max(0.0, (x**k+y**k-0.5**k))**(1/k)

    @staticmethod
    def _maybeFunction(x: float, y: float, k: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        val = (x**k+y**k-0.5**k)**(1/k)
        if val < 0:
            return 0.0
        elif val > 1:
            return 1.0
        else:
            return val

    @staticmethod
    def getMarker(k: float) -> {}:
        upper_marker_x, upper_marker_y = AggregationFunction.findMarkerFromFunction(k, 1, 1, 1, -0.01, LukasiewiczAggregationFunction._yesFunction, True)
        lower_marker_x, lower_marker_y = AggregationFunction.findMarkerFromFunction(k, 0, 0, 0, 0.01, LukasiewiczAggregationFunction._noFunction, True)
        right_marker_x, right_marker_y = AggregationFunction.findMarkerFromFunction(k, 1, 1, 1, -0.01, LukasiewiczAggregationFunction._yesFunction, False)
        left_marker_x, left_marker_y = AggregationFunction.findMarkerFromFunction(k, 0, 0, 0, 0.01, LukasiewiczAggregationFunction._noFunction, False)

        return {'ux': upper_marker_x, 'uy': upper_marker_y, 'lox': lower_marker_x, 'loy': lower_marker_y,
                'rx': right_marker_x, 'ry': right_marker_y, 'lx': left_marker_x, 'ly': left_marker_y}


class MinMaxAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, k: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return MinMaxAggregationFunction._noFunction(x, y)
        elif x < 0.5 or y < 0.5:
            return MinMaxAggregationFunction._maybeFunction(x, y)
        elif x >= 0.5 and y >= 0.5:
            return MinMaxAggregationFunction._yesFunction(x, y)

    @staticmethod
    def _yesFunction(x: float, y: float, k: float) -> float:
        return max(x, y)

    @staticmethod
    def _noFunction(x: float, y: float, k: float) -> float:
        return min(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float, k: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return x**k+y**k-0.5**k


class TnormTconormAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float, k: float = 1) -> float:
        if x < 0.5 and y < 0.5:
            return TnormTconormAggregationFunction._noFunction(x, y)
        elif x < 0.5 or y < 0.5:
            return TnormTconormAggregationFunction._maybeFunction(x, y)
        elif x >= 0.5 and y >= 0.5:
            return TnormTconormAggregationFunction._yesFunction(x, y)

    @staticmethod
    def _yesFunction(x: float, y: float, k: float) -> float:
        return -1+2*x+2*y-2*x*y

    @staticmethod
    def _noFunction(x: float, y: float, k: float) -> float:
        return TnormTconormAggregationFunction._maybeFunction(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float, k: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return 2*x*y
