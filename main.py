import sys
import tkinter
import tkinter.filedialog as tkFile
import tkinter as tk

import numpy
import numpy as np
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import os.path as path

import AggregationFunction


# Trash code
class MyView:

    btn_width = 10

    def __init__(self):
        self.data = []

        self.root = tk.Tk()
        self.root.title("Project 19")
        self.root.geometry("600x400")

        # Input
        self.containerInput = tk.Frame(master=self.root, width=150)

        self.txtFileName = tk.Label(master=self.containerInput, text="File Name")

        self.btnLoadFile = tk.Button(master=self.containerInput,
                                     text="Load File",
                                     width=self.btn_width,
                                     command=self.open_file)

        self.btnPlot = tk.Button(master=self.containerInput,
                                 text="Plot",
                                 width=self.btn_width,
                                 command=lambda: self.plot("sell", "time"))

        self.invertX = tkinter.BooleanVar()
        self.cbInvertX = tk.Checkbutton(master=self.containerInput, text="X Inverted", variable=self.invertX)
        self.invertY = tkinter.BooleanVar()
        self.cbInvertY = tk.Checkbutton(master=self.containerInput, text="Y Inverted", variable=self.invertY)

        self.gridExtremes = tk.Frame(master=self.containerInput)

        self.txtExtremesX = tk.Label(master=self.gridExtremes, text="X")
        self.txtExtremesY = tk.Label(master=self.gridExtremes, text="Y")

        self.txtMinX = tk.Label(master=self.gridExtremes, text="Min")
        self.txtMaxX = tk.Label(master=self.gridExtremes, text="Max")
        self.txtMinY = tk.Label(master=self.gridExtremes, text="Min")
        self.txtMaxY = tk.Label(master=self.gridExtremes, text="Max")

        self.entMinX = tk.Entry(master=self.gridExtremes, width=6)
        self.entMinY = tk.Entry(master=self.gridExtremes, width=6)
        self.entMaxY = tk.Entry(master=self.gridExtremes, width=6)
        self.entMaxX = tk.Entry(master=self.gridExtremes, width=6)

        # Create a Tkinter variable
        self.aggregationPopupValue = tk.StringVar(self.containerInput)
        # Dictionary with options
        choices = {'Lukasiewicz', 'MinMax', 'TnormTconorm'}
        self.aggregationPopupValue.set('Lukasiewicz')  # set the default option

        self.aggregationPopup = tk.OptionMenu(self.containerInput, self.aggregationPopupValue, *choices)
        txtAggregationLabel = tk.Label(master=self.containerInput, text="Aggregation Function")

        self.txtExtremesX.grid(row=1, column=0)
        self.txtMinX.grid(row=0, column=1)
        self.txtMaxX.grid(row=0, column=2)
        self.entMinX.grid(row=1, column=1)
        self.entMaxX.grid(row=1, column=2)

        self.txtExtremesY.grid(row=4, column=0)
        self.txtMinY.grid(row=3, column=1)
        self.txtMaxY.grid(row=3, column=2)
        self.entMinY.grid(row=4, column=1)
        self.entMaxY.grid(row=4, column=2)

        self.btnLoadFile.pack()
        self.txtFileName.pack()
        self.btnPlot.pack()

        self.gridExtremes.pack(fill=tk.X, anchor=tk.NW)

        self.cbInvertX.pack()
        self.cbInvertY.pack()

        txtAggregationLabel.pack()
        self.aggregationPopup.pack()

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

    def getEntryValue(self, entry, default: float) -> float:
        value = entry.get()
        if value != "":
            return float(value)
        else:
            entry.delete(0, tk.END)
            entry.insert(0, default)
            return default

    def plot(self, x_key: str, y_key: str):

        self.targetSubPlot.clear()

        plot_targets = []

        extreme_x_min = self.getEntryValue(self.entMinX, 400)
        extreme_x_max = self.getEntryValue(self.entMaxX, 600)
        extreme_y_min = self.getEntryValue(self.entMinY, 8)
        extreme_y_max = self.getEntryValue(self.entMaxY, 12)

        # TODO: get from UI
        inverse_x = self.invertX.get()
        inverse_y = self.invertY.get()

        # get selected aggregation function
        aggregation_function = AggregationFunction.AggregationFunction.getClassFromString(self.aggregationPopupValue.get())

        min_x = sys.float_info.max
        max_x = sys.float_info.min
        min_y = sys.float_info.max
        max_y = sys.float_info.min

        # get min and max values
        for val in self.data:
            x = val[x_key]
            y = val[y_key]

            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x

            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y

        # set boundaries from extreme values
        if max_x > extreme_x_max:
            max_x = extreme_x_max
        if min_x < extreme_x_min:
            min_x = extreme_x_min
        if max_y > extreme_y_max:
            max_y = extreme_y_max
        if min_y < extreme_y_min:
            min_y = extreme_y_min

        # apply min_max_normalization
        for val in self.data:
            # get x values ensure value is within boundaries
            x_val = val[x_key]
            if x_val > extreme_x_max:
                x_val = extreme_x_max
            elif x_val < extreme_x_min:
                x_val = extreme_x_min

            # get y values ensure value is within boundaries
            y_val = val[y_key]
            if y_val > extreme_y_max:
                y_val = extreme_y_max
            elif y_val < extreme_y_min:
                y_val = extreme_y_min

            # apply min max normalization
            target_x = (x_val - min_x)/(max_x - min_x)
            target_y = (y_val - min_y)/(max_y - min_y)

            # inverse for plot if necessary
            if inverse_x:
                target_x = 1 - target_x
            if inverse_y:
                target_y = 1 - target_y


            # get value from aggregation function
            point_value = aggregation_function.perform(target_x, target_y)

            color: str
            if point_value == 0:
                color = "red"
            elif point_value == 1:
                color = "green"
            else:
                color = "gray"

            plot_targets.append({"x": target_x, "y": target_y, "val": point_value, "color": color})

        # prepare lists for each axis and the color
        x_targets = []
        y_targets = []
        color_targets = []
        for target in plot_targets:
            x_targets.append(target["x"])
            y_targets.append(target["y"])
            color_targets.append(target["color"])

        # plot scatter plot
        sc = self.targetSubPlot.scatter(x_targets, y_targets, color=color_targets)

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
                    # get correct value
                    value = plot_targets[ind["ind"][0]]["val"]

                    # set annotation position
                    pos = sc.get_offsets()[ind["ind"][0]]
                    annot.xy = pos

                    # set annotation text
                    annot.set_text(str(value))
                    annot.get_bbox_patch().set_alpha(0.4)

                    # set visible and redraw
                    annot.set_visible(True)
                    self.canvasPlot.draw_idle()
                else:
                    # hide annotation and redraw
                    annot.set_visible(False)
                    self.canvasPlot.draw_idle()

        # set on hover event
        self.canvasPlot.mpl_connect('motion_notify_event', on_plot_hover)

        self.targetSubPlot.set_xlim(0, 1)
        self.targetSubPlot.set_ylim(0, 1)
        # self.targetSubPlot.set_xlim(-0.05, 1.05)
        # self.targetSubPlot.set_ylim(-0.05, 1.05)
        # self.targetSubPlot.set_xticks(10)
        # self.targetSubPlot.set_yticks(10)

        # draw lines for the 4 sections
        self.targetSubPlot.axhline(y=0.5, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=0.5, color='black', linestyle='dotted', linewidth=1)
        # self.targetSubPlot.plot([0, 0.5], [0.5, 0], color='black', linestyle='dotted', linewidth=1)

        # draw the data
        self.canvasPlot.draw()

    def run(self):
        self.root.mainloop()

    # source: https://realpython.com/python-gui-tkinter/#building-a-text-editor-example-app
    def open_file(self) -> bool:

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

                    if index == 0:
                        value_dict[keys[index]] = entry.strip()
                    else:
                        value_dict[keys[index]] = float(entry.strip())

                self.data.append(value_dict)

        return True


def main():
    MyView().run()


if __name__ == "__main__":
    main()
