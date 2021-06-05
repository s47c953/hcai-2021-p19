import sys
import tkinter
import tkinter.filedialog as tkFile
import tkinter.ttk
import tkinter as tk

import numpy
import numpy as np
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import os.path as path

import AggregationFunction
import UITools
import filehandler
import model
import view


# Trash code
class Main:

    main_view: view.View

    def __init__(self):
        # data fields
        self.input_data = None
        self.bounds = None
        self.normalized_data = None
        self.data_coordination = None
        self.keys = None

        # view
        self.main_view = view.View()

        # button callbacks
        cmnd = "command"
        self.main_view.btnCalcLR[cmnd] = self.calc_lambdaR
        self.main_view.btnLoadFile[cmnd] = self.load
        self.main_view.btnChangeValue[cmnd] = self.changeInputData
        self.main_view.btnPlot[cmnd] = self.plot

    def run(self):
        self.main_view.run()

    def load(self):

        # 1. load data
        res, data, bounds, keys = filehandler.open_file(self.main_view.txtFileName)

        if not res:
            return

        self.main_view.data_loaded = True

        # 2. normalize data
        normalized = model.normalizeInputData(data, bounds)

        # 3. store on class member
        self.input_data = data
        self.bounds = bounds
        self.normalized_data = normalized
        self.keys = keys

        return

    def changeInputData(self):
        self.input_data[self.main_view.selected_node_index]["value"] = float(self.main_view.entInputSol.get())

    def addUserInputData(self):
        x = float(self.main_view.entInputX.get())
        y = float(self.main_view.entInputY.get())

        self.data_coordination.append({"x": x, "y": y})
        self.plot()

    def clear(self):
        self.input_data.clear()
        self.bounds.clear()
        self.normalized_data.clear()
        self.data_coordination.clear()
        self.calc_lambdaR()
        self.plot()

    def plot(self):
        inverse_x = self.main_view.invertX.get()
        inverse_y = self.main_view.invertY.get()

        l = float(self.main_view.entK.get())
        r = float(self.main_view.entR.get())
        # get selected aggregation function
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(
            self.main_view.aggregationPopupValue.get())

        x_keys = ["Distance Schools", "Distance Grocery Shop", "Distance Motorway", "Distance Public Transport"]
        y_keys = ["Size", "Garten Size", "Rooms", "Price"]
        # x_keys = ["P1", "P2", "P3"]
        # y_keys = ["P4", "P5", "P6", "P7"]
        aggr_data = model.aggregateData(self.normalized_data, x_keys, y_keys, "mostof", "mostof", 0.5, 0.85)

        # calculate sum of values for plotting
        plot_targets, value_sum = UITools.preparePlotTargets(aggr_data, False, False,
                                                             aggregation_function, l, r)

        # plot the sum of values
        self.main_view.txtSumValue.set("{:.4f}".format(value_sum))
        self.main_view.plot(plot_targets, self.normalized_data, self.input_data, aggregation_function, l, r)

    def calc_lambdaR(self):
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(self.main_view.aggregationPopupValue.get())
        l_mean, r_mean, l, r = aggregation_function.getLambdaR(self.normalized_data, 0.0001, 2, 0.0001, 2, 0.0001)

        self.main_view.entR.delete(0, "end")
        self.main_view.entR.insert(0, "{:.4f}".format(r))
        self.main_view.entK.delete(0, "end")
        self.main_view.entK.insert(0, "{:.4f}".format(l))
        self.main_view.entErrorL.delete(0, "end")
        self.main_view.entErrorL.insert(0, "{:.4f}".format(l_mean))
        self.main_view.entErrorR.delete(0, "end")
        self.main_view.entErrorR.insert(0, "{:.4f}".format(r_mean))
        pass


if __name__ == "__main__":
    Main().run()
