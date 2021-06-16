from model.Model import Model
from model.Filehandler import open_file
from view.View import View


class Controller:

    def __init__(self, model: Model, view: View):
        # MVC classes
        self.model = model
        self.view = view

        # object to keep track of loaded data
        self.raw_data = None
        self.normalized_data = None
        self.quantified_data = None
        self.keys = None
        self.bounds = None
        self.target_values = {}

        # register event handler
        self.view.registerLoadFileEvent(self.loadFile)
        self.view.registerClearEvent(self.clearData)
        self.view.registerQuantifierButtonEvent(lambda: self.view.quantifierViewWrapper(self.keys))
        self.view.registerPlotEvent(self.plotData)
        self.view.registerCalcLREvent(self.calculateLambdaR)
        self.view.registerSetValueEvent(self.changeTargetValue)

    def loadFile(self):
        label_string, data, bounds, keys = open_file()
        self.view.setLabelFileText(label_string)
        normalized_data = self.model.normalizeInputData(data, bounds)
        self.raw_data = data
        self.normalized_data = normalized_data
        self.keys = keys
        self.bounds = bounds

    def clearData(self):
        self.raw_data = None
        self.normalized_data = None
        self.quantified_data = None
        self.keys = None
        self.bounds = None
        self.target_values = {}
        self.calculateLambdaR()
        self.plotData()

    def plotData(self):
        # get data for applying quantifier functions
        x_keys, y_keys = self.view.getQuantifierAxes()
        x_mode, y_mode = self.view.getQuantifierModes()
        m, n = self.view.getQuantifierMN()

        self.quantified_data = self.model.ApplyQuantifierFunction(self.normalized_data, x_keys, y_keys, x_mode, y_mode, m, n)
        self.quantified_data = self.model.restoreTargetValues(self.quantified_data, self.target_values)

        # get aggregation parameter
        l, r = self.view.getLambdaR()
        selected_aggregation_function = self.view.getSelectedAggregationFunction()
        aggregation_function = self.model.getAggregationFunctionFromString(selected_aggregation_function)

        plot_targets, value_sum = self.model.preparePlotTargets(self.quantified_data, aggregation_function, l, r)
        self.view.setSumValue(value_sum)
        self.view.plot(plot_targets, self.quantified_data, self.raw_data, aggregation_function, l, r)

    def changeTargetValue(self):
        selected_node = self.view.getSelectedNoteIndex()
        target_value = self.view.getTargetNodeValue()
        self.target_values[selected_node] = target_value
        self.quantified_data[selected_node]["value"] = target_value

    def calculateLambdaR(self):
        selected_aggregation_function = self.view.getSelectedAggregationFunction()
        aggregation_function = self.model.getAggregationFunctionFromString(selected_aggregation_function)
        l_mean, r_mean, l, r = aggregation_function.getLambdaR(self.quantified_data, -2.0, 4.0, 0.0001, 5.0, 0.0001)
        self.view.setLambdaR(l, r, l_mean, r_mean)
