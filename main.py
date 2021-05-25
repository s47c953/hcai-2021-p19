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

        # view
        self.main_view = view.View()

        # button callbacks
        self.main_view.btnCalcLR["command"] = self.calc_lambdaR
        self.main_view.btnLoadFile["command"] = self.load
        self.main_view.btnChangeValue["command"] = self.changeInputData

    def run(self):
        self.main_view.run()

    def load(self):

        # 1. load data
        data, bounds = filehandler.open_file(self.main_view.txtFileName)

        # 2. normalize data
        normalized = model.normalizeInputData(data, bounds)

        # 3. store on class member
        self.input_data = data
        self.bounds = bounds
        self.normalized_data = normalized

        return

    def changeInputData(self):
        self.data[self.main_view.selected_node_index]["value"] = float(self.entInputSol.get())

    def addUserInputData(self):
        x = float(self.entInputX.get())
        y = float(self.entInputY.get())

        self.data.append({"x": x, "y": y})
        self.plot("x", "y")

    @staticmethod
    def getEntryValue(entry, default: float) -> float:
        value = entry.get()
        if value != "":
            return float(value)
        else:
            entry.delete(0, tk.END)
            entry.insert(0, default)
            return default

    def clear(self):
        self.data.clear()
        self.calc_lambdaR()
        self.plot("x", "y")

    def plot(self, x_key: str, y_key: str):
        self.targetSubPlot.clear()
        plot_targets = []

        # TODO: get from UI
        inverse_x = self.invertX.get()
        inverse_y = self.invertY.get()

        l = float(self.entK.get())
        r = float(self.entR.get())

        # get selected aggregation function
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(self.aggregationPopupValue.get())

        # calculate sum of values for plotting
        plot_targets, value_sum = UITools.preparePlotTargets(self.data, x_key, y_key, inverse_x, inverse_y,
                                                             aggregation_function, l, r)

        # plot the sum of values
        self.txtSumValue.set("{:.4f}".format(value_sum))

        # prepare lists for each axis and the color
        x_targets = []
        y_targets = []
        color_targets = []
        border_targets = []
        for i, target in enumerate(plot_targets):
            x_targets.append(target["x"])
            y_targets.append(target["y"])
            color_targets.append(target["color"])
            if i == self.selected_index:
                border_targets.append("blue")
            elif target["is_training_point"]:
                border_targets.append("white")
            else:
                border_targets.append("black")

        # plot scatter plot
        sc = self.targetSubPlot.scatter(x_targets, y_targets, color=color_targets, edgecolors=border_targets)

        # create annotation object and hide it
        annot = self.targetSubPlot.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                            bbox=dict(boxstyle="round", fc="w"),
                                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        # hover event for nodes
        def on_plot_hover(event):
            if event.inaxes == self.targetSubPlot:
                cont, ind = sc.contains(event)
                if cont:
                    index = ind["ind"][0]
                    # get correct value
                    value = plot_targets[index]["val"]
                    if "sol" in self.data[index]:
                        target = self.data[index]["sol"]
                    else:
                        target = "not defined"

                    # set annotation position
                    pos = sc.get_offsets()[index]
                    annot.xy = pos

                    # set annotation text
                    annot.set_text(f"{pos}\ntarget: {target}\ncalculated: {value}")
                    annot.get_bbox_patch().set_alpha(0.4)

                    # set visible and redraw
                    annot.set_visible(True)
                    self.canvasPlot.draw_idle()
                else:
                    # hide annotation and redraw
                    annot.set_visible(False)
                    self.canvasPlot.draw_idle()

        def on_node_click(event):
            if event.inaxes == self.targetSubPlot:
                cont, ind = sc.contains(event)
                if cont:
                    # get correct value
                    index = ind["ind"][0]
                    x = self.data[index]["x"]
                    y = self.data[index]["y"]
                    if "sol" in self.data[index]:
                        sol = self.data[index]["sol"]
                    else:
                        sol = -1

                    self.entInputX.delete(0, "end")
                    self.entInputX.insert(0, "{:.4f}".format(x))
                    self.entInputY.delete(0, "end")
                    self.entInputY.insert(0, "{:.4f}".format(y))
                    self.entInputSol.delete(0, "end")
                    self.entInputSol.insert(0, "{:.4f}".format(sol))
                    self.selected_index = index
                    self.plot("x", "y")

        # set on hover event
        if self.hoover_cid:
            self.canvasPlot.mpl_disconnect(self.hoover_cid)
        if self.click_cid:
            self.canvasPlot.mpl_disconnect(self.click_cid)
        self.hoover_cid = self.canvasPlot.mpl_connect('motion_notify_event', on_plot_hover)
        self.click_cid = self.canvasPlot.mpl_connect('button_press_event', on_node_click)

        self.targetSubPlot.set_xlim(0, 1)
        self.targetSubPlot.set_ylim(0, 1)
        self.targetSubPlot.set_xlim(-0.05, 1.05)
        self.targetSubPlot.set_ylim(-0.05, 1.05)
        # self.targetSubPlot.set_xticks(10)
        # self.targetSubPlot.set_yticks(10)

        # draw lines for the 4 sections
        marker_x_yes, marker_y_yes, marker_x_no, marker_y_no = aggregation_function.getMarker(l)
        self.targetSubPlot.axhline(y=0.5, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axhline(y=0, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axhline(y=1, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=0.5, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=0, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=1, color='gray', linestyle='dotted', linewidth=1)
        # self.targetSubPlot.plot([0, 0.5], [0.5, 0], color='black', linestyle='dotted', linewidth=1)

        # draw yes-no borders
        self.targetSubPlot.plot(marker_x_yes, marker_y_yes, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.plot(marker_x_no, marker_y_no, color='black', linestyle='dotted', linewidth=1)

        # draw the data
        self.canvasPlot.draw()

    def calc_lambdaR(self):
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(self.main_view.aggregationPopupValue.get())
        l_mean, r_mean, l, r = aggregation_function.getLambdaR(self.data, 0.0001, 2, 0.0001, 2, 0.0001)

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
