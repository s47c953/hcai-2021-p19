
# abstract base
class AggregationFunction:
    @staticmethod
    def perform(x: float, y: float) -> float:
        raise NotImplementedError


class LukasiewiczAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float) -> float:
        if x < 0.5 and y < 0.5:
            return LukasiewiczAggregationFunction._noFunction(x, y)
        elif x < 0.5 or y < 0.5:
            return LukasiewiczAggregationFunction._maybeFunction(x, y)
        elif x >= 0.5 and y >= 0.5:
            return LukasiewiczAggregationFunction._yesFunction(x, y)

    @staticmethod
    def _yesFunction(x: float, y: float) -> float:
        return min(1.0, x+y-0.5)

    @staticmethod
    def _noFunction(x: float, y: float) -> float:
        return max(0, x+y-0.5)

    @staticmethod
    def _maybeFunction(x: float, y: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        val = x+y-0.5
        if val < 0:
            return 0.0
        elif val > 1:
            return 1.0
        else:
            return val


class MinMaxAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float) -> float:
        if x < 0.5 and y < 0.5:
            return MinMaxAggregationFunction._noFunction(x, y)
        elif x < 0.5 or y < 0.5:
            return MinMaxAggregationFunction._maybeFunction(x, y)
        elif x >= 0.5 and y >= 0.5:
            return MinMaxAggregationFunction._yesFunction(x, y)

    @staticmethod
    def _yesFunction(x: float, y: float) -> float:
        return max(x, y)

    @staticmethod
    def _noFunction(x: float, y: float) -> float:
        return min(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return x+y-0.5


class TnormTconormAggregationFunction(AggregationFunction):
    @staticmethod
    def perform(x: float, y: float) -> float:
        if x < 0.5 and y < 0.5:
            return TnormTconormAggregationFunction._noFunction(x, y)
        elif x < 0.5 or y < 0.5:
            return TnormTconormAggregationFunction._maybeFunction(x, y)
        elif x >= 0.5 and y >= 0.5:
            return TnormTconormAggregationFunction._yesFunction(x, y)

    @staticmethod
    def _yesFunction(x: float, y: float) -> float:
        return -1+2*x+2*y-2*x*y

    @staticmethod
    def _noFunction(x: float, y: float) -> float:
        return TnormTconormAggregationFunction._maybeFunction(x, y)

    @staticmethod
    def _maybeFunction(x: float, y: float) -> float:
        # TODO: check if real median or just middle value of 0, 1, x+y-1/2 is needed
        return 2*x*y