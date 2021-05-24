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


# Trash code
class MyView:
    btn_width = 10

    def __init__(self):
        self.data = []

        self.root = tk.Tk()
        self.root.title("Project 19")
        self.root.geometry("800x600")

        self.selected_index = -1

        # IDs of eventhandle, needed to be unregistered on new plot
        self.hoover_cid = None
        self.click_cid = None

        # Input
        self.containerInput = tk.Frame(master=self.root, width=150)

        # file loading elements
        self.txtFileName = tk.Label(master=self.containerInput, text="File Name")
        self.btnLoadFile = tk.Button(master=self.containerInput,
                                     text="Load File",
                                     width=self.btn_width,
                                     command=self.open_file)
        self.btnLoadFile.pack()
        self.txtFileName.pack()

        # Aggregation Dropdown
        self.aggregationPopupValue = tk.StringVar(self.containerInput)
        # Dictionary with options
        choices = {'Lukasiewicz', 'MinMax', 'TnormTconorm'}
        self.aggregationPopupValue.set('Lukasiewicz')  # set the default option

        self.aggregationPopup = tk.OptionMenu(self.containerInput, self.aggregationPopupValue, *choices)
        txtAggregationLabel = tk.Label(master=self.containerInput, text="Aggregation Function")
        txtAggregationLabel.pack()
        self.aggregationPopup.pack()

        # lambda and r
        self.gridLambdaR = tk.Frame(master=self.containerInput)
        tk.Label(master=self.gridLambdaR, text="l: ").grid(row=0, column=0)
        tk.Label(master=self.gridLambdaR, text="r: ").grid(row=1, column=0)
        tk.Label(master=self.gridLambdaR, text="mean error l: ").grid(row=2, column=0)
        tk.Label(master=self.gridLambdaR, text="mean error r: ").grid(row=3, column=0)
        self.entK = tk.Entry(master=self.gridLambdaR, width=6)
        self.entK.insert(0, 1.0)
        self.entK.grid(row=0, column=1)
        self.entR = tk.Entry(master=self.gridLambdaR, width=6)
        self.entR.insert(0, 1.0)
        self.entR.grid(row=1, column=1)
        self.entErrorL = tk.Entry(master=self.gridLambdaR, width=6)
        self.entErrorL.insert(0, 0.0)
        self.entErrorL.grid(row=2, column=1)
        self.entErrorR = tk.Entry(master=self.gridLambdaR, width=6)
        self.entErrorR.insert(0, 0.0)
        self.entErrorR.grid(row=3, column=1)
        self.gridLambdaR.pack()

        # calc lambda and r
        self.btnCalcLR = tk.Button(master=self.containerInput,
                                   text="calc l r",
                                   width=self.btn_width,
                                   command=self.calc_lambdaR)
        self.btnCalcLR.pack()

        # plotting trigger button
        self.btnPlot = tk.Button(master=self.containerInput,
                                 text="Plot",
                                 width=self.btn_width,
                                 command=lambda: self.plot("x", "y"))
        self.btnPlot.pack()

        # clear data trigger button
        self.btnClear = tk.Button(master=self.containerInput,
                                  text="Clear",
                                  width=self.btn_width,
                                  command=self.clear)
        self.btnClear.pack()

        # inverting checkboxes
        self.invertX = tkinter.BooleanVar()
        self.cbInvertX = tk.Checkbutton(master=self.containerInput, text="X Inverted", variable=self.invertX)
        self.invertY = tkinter.BooleanVar()
        self.cbInvertY = tk.Checkbutton(master=self.containerInput, text="Y Inverted", variable=self.invertY)
        self.cbInvertX.pack()
        self.cbInvertY.pack()

        # user input for points
        self.gridInput = tk.Frame(master=self.containerInput)
        self.txtInputX = tk.Label(master=self.gridInput, text="X")
        self.txtInputY = tk.Label(master=self.gridInput, text="Y")
        self.txtInputSol = tk.Label(master=self.gridInput, text="Sol")
        self.entInputX = tk.Entry(master=self.gridInput, width=6)
        self.entInputY = tk.Entry(master=self.gridInput, width=6)
        self.entInputSol = tk.Entry(master=self.gridInput, width=6)
        self.txtInputX.grid(row=0, column=0)
        self.txtInputY.grid(row=1, column=0)
        self.txtInputSol.grid(row=2, column=0)
        self.entInputX.grid(row=0, column=1)
        self.entInputY.grid(row=1, column=1)
        self.entInputSol.grid(row=2, column=1)
        self.gridInput.pack(fill=tk.X, anchor=tk.NW)

        self.btnAddValue = tk.Button(master=self.containerInput,
                                     text="Add",
                                     width=self.btn_width,
                                     command=self.addUserInputData)

        self.btnChangeValue = tk.Button(master=self.containerInput,
                                        text="Change",
                                        width=self.btn_width,
                                        command=self.changeInputData)
        self.btnAddValue.pack()
        self.btnChangeValue.pack()

        # sum of all nodes
        self.gridSum = tk.Frame(master=self.containerInput)
        tk.Label(master=self.gridSum, text="Sum: ").grid(row=0, column=0)
        self.txtSumValue = tk.StringVar()
        self.txtSumValue.set(0)
        lblSumValue = tk.Label(master=self.gridSum, textvariable=self.txtSumValue)
        lblSumValue.grid(row=0, column=1)
        self.gridSum.pack(fill=tk.X, anchor=tk.NW)

        self.containerInput.pack(fill=tk.Y, side=tk.LEFT)
        self.containerInput.pack_propagate(0)

        # Plot
        self.containerPlot = tk.Frame(master=self.root)
        self.containerPlot.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.i = tk.Label(master=self.containerPlot, text="The Plot:")
        self.i.pack()

        self.figurePlot = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.targetSubPlot = self.figurePlot.add_subplot(111)
        self.targetSubPlot.set_xticks(numpy.arange(0, 1.1, 0.1))
        self.targetSubPlot.set_yticks(numpy.arange(0, 1.1, 0.1))

        self.canvasPlot = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.figurePlot, master=self.containerPlot)
        self.canvasPlot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def changeInputData(self):
        self.data[self.selected_index]["sol"] = float(self.entInputSol.get())

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

    def run(self):
        self.root.mainloop()

    def calc_lambdaR(self):
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(self.aggregationPopupValue.get())
        l_mean, r_mean, l, r = aggregation_function.getLambdaR(self.data, 0.0001, 2, 0.0001, 2, 0.0001)

        self.entR.delete(0, "end")
        self.entR.insert(0, "{:.4f}".format(r))
        self.entK.delete(0, "end")
        self.entK.insert(0, "{:.4f}".format(l))
        self.entErrorL.delete(0, "end")
        self.entErrorL.insert(0, "{:.4f}".format(l_mean))
        self.entErrorR.delete(0, "end")
        self.entErrorR.insert(0, "{:.4f}".format(r_mean))
        pass

    # source: https://realpython.com/python-gui-tkinter/#building-a-text-editor-example-app
    def open_file(self) -> bool:

        # clearing is now done explicit via UI
        # self.data.clear()
        """Open a file for editing."""
        filepath = tkFile.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not filepath:
            self.txtFileName.config(text="File not found!")
            return False

        # self.p.config(text=path.basename(filepath))
        self.txtFileName["text"] = "File Name: " + path.basename(filepath)

        with open(filepath, "r") as input_file:
            file = input_file.readlines()

            keys: []

            for lineNr, line in enumerate(file):
                entries = line.strip().split(", ")

                if lineNr == 0:
                    keys = entries
                    continue

                value_dict = {}

                for index, entry in enumerate(entries):
                    # if index == 0:
                    #     value_dict[keys[index]] = entry.strip()
                    # else:
                    value_dict[keys[index]] = float(entry.strip())

                self.data.append(value_dict)

        return True


def main():
    MyView().run()


if __name__ == "__main__":
    main()
