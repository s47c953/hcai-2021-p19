import tkinter as tk
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import numpy
from PIL import Image

from view.QuantifierView import QuantifierView


class View:

    # UI constants
    BUTTON_WIDTH = 10

    def __init__(self):

        # ---- helper member for UI state ---- #
        # index of selected node in plot
        self.selected_node_index = None
        # IDs of eventhandler, needed to be unregistered on new plot
        self.hoover_cid = None
        self.click_cid = None

        # ---- Draw UI ---- #
        self.root = tk.Tk()
        self.root.title("Project 19")
        self.root.geometry("800x600")

        # Input Section
        self.containerInput = tk.Frame(master=self.root, width=150)

        # Data loading
        self.txtFileName = tk.Label(master=self.containerInput, text="File Name")
        self.btnLoadFile = tk.Button(master=self.containerInput,
                                     text="Load File",
                                     width=self.BUTTON_WIDTH)
        self.btnLoadFile.pack()
        self.txtFileName.pack()

        # Query Builder
        self.aqView = QuantifierView()
        self.btnQueryWindow = tk.Button(master=self.containerInput,
                                        text="Query",
                                        width=self.BUTTON_WIDTH)
        self.btnQueryWindow.pack()

        # Aggregation Dropdown
        self.aggregationPopupValue = tk.StringVar(self.containerInput)
        # Dictionary with options
        choices = {'Lukasiewicz', 'MinMax', 'TnormTconorm'}
        self.aggregationPopupValue.set('Lukasiewicz')  # set the default option
        self.aggregationPopup = tk.OptionMenu(self.containerInput, self.aggregationPopupValue, *choices)
        self.txtAggregationLabel = tk.Label(master=self.containerInput, text="Aggregation Function")
        self.txtAggregationLabel.pack()
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
        self.entErrorL = tk.Label(master=self.gridLambdaR, text="0.0")
        self.entErrorL.grid(row=2, column=1)
        self.entErrorR = tk.Label(master=self.gridLambdaR, text="0.0")
        self.entErrorR.grid(row=3, column=1)
        self.gridLambdaR.pack()

        # button for calculating lambda and r
        self.btnCalcLR = tk.Button(master=self.containerInput,
                                   text="calc l r",
                                   width=self.BUTTON_WIDTH)
        self.btnCalcLR.pack()

        # button to trigger the plotting
        self.btnPlot = tk.Button(master=self.containerInput,
                                 text="Plot",
                                 width=self.BUTTON_WIDTH)
        self.btnPlot.pack()

        # clear data trigger button
        self.btnClear = tk.Button(master=self.containerInput,
                                  text="Clear",
                                  width=self.BUTTON_WIDTH)
        self.btnClear.pack()

        # user input for point manipulaition
        self.gridInput = tk.Frame(master=self.containerInput)
        tk.Label(master=self.gridInput, text="x").grid(row=0, column=0)
        tk.Label(master=self.gridInput, text="y").grid(row=1, column=0)
        self.lblX = tk.Label(master=self.gridInput, width=6)
        self.lblY = tk.Label(master=self.gridInput, width=6)
        tk.Label(master=self.gridInput, text="Target: ").grid(row=2, column=0)
        self.lblX.grid(row=0, column=1)
        self.lblY.grid(row=1, column=1)
        self.entInputSol = tk.Entry(master=self.gridInput, width=6)
        self.entInputSol.grid(row=2, column=1)
        self.gridInput.pack(fill=tk.X, anchor=tk.NW)

        self.btnSetValue = tk.Button(master=self.containerInput,
                                        text="Set",
                                        width=self.BUTTON_WIDTH)
        self.btnSetValue.pack()

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

        # Plot section
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

    def quantifierViewWrapper(self, keys: list):
        self.aqView.open_query_window(keys)

    def registerLoadFileEvent(self, event):
        self.btnLoadFile["command"] = event

    def registerQuantifierButtonEvent(self, event):
        self.btnQueryWindow["command"] = event

    def registerCalcLREvent(self, event):
        self.btnCalcLR["command"] = event

    def registerPlotEvent(self, event):
        self.btnPlot["command"] = event

    def registerClearEvent(self, event):
        self.btnClear["command"] = event

    def registerSetValueEvent(self, event):
        self.btnSetValue["command"] = event

    def setLabelFileText(self, text: str):
        self.txtFileName["text"] = text

    def setLambdaR(self, l: float, r: float, l_error: float, r_error: float):
        self.entR.delete(0, "end")
        self.entR.insert(0, "{:.4f}".format(r))
        self.entK.delete(0, "end")
        self.entK.insert(0, "{:.4f}".format(l))
        self.entErrorL["text"] = "{:.4f}".format(l_error)
        self.entErrorR["text"] = "{:.4f}".format(r_error)

    def setSumValue(self, value: float):
        self.txtSumValue.set("{:.4f}".format(value))

    def getLambdaR(self) -> (float, float):
        l = float(self.entK.get())
        r = float(self.entR.get())
        return l, r

    def getQuantifierAxes(self) -> (list, list):
        x_keys = self.aqView.keys_x
        y_keys = self.aqView.keys_y
        return x_keys, y_keys

    def getQuantifierMN(self) -> (float, float):
        m = self.aqView.m
        n = self.aqView.n
        return m, n

    def getQuantifierModes(self) -> (str, str):
        x_mode = self.aqView.x_mode
        y_mode = self.aqView.y_mode
        return x_mode, y_mode

    def getSelectedAggregationFunction(self) -> str:
        return self.aggregationPopupValue.get()

    def getSelectedNoteIndex(self) -> int:
        return self.selected_node_index

    def getTargetNodeValue(self) -> float:
        return float(self.entInputSol.get())

    def run(self):
        self.root.mainloop()

    def createBackground(self, aggregation_function, l, r):
        resolution = 250

        # gradient between 0 and 1 for 256*256
        array = numpy.empty((resolution, resolution, 3), numpy.uint8)


        for y in range(0, resolution):
            for x in range(0, resolution):
                value = aggregation_function.perform(x/resolution, y/resolution, l, r)
                # add blue color to maybe points
                if value != 0 and value != 1:
                    blue_val = 44
                else:
                    blue_val = 00

                red_val = 255 - int(255 * value)
                green_val = int(255 * value)
                array[resolution-y-1][x] = [red_val, green_val, blue_val]


        # Creates PIL image
        img = Image.fromarray(array, 'RGB')
        return img


    def plot(self, plot_targets: [], data: [], aggregation_function, l, r):
        self.targetSubPlot.clear()

        # prepare lists for each axis and the color
        x_targets = []
        y_targets = []
        color_targets = []
        border_targets = []
        for i, target in enumerate(plot_targets):
            x_targets.append(target["x"])
            y_targets.append(target["y"])
            color_targets.append(target["color"])
            if i == self.selected_node_index:
                border_targets.append("blue")
            elif target["is_training_point"]:
                border_targets.append("white")
            else:
                border_targets.append("black")



        img = self.createBackground(aggregation_function, l, r)
        self.targetSubPlot.imshow(img, extent=[0, 1, 0, 1])
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
                    if "value" in data[index]:
                        target = data[index]["value"]
                    else:
                        target = "not defined"
                    if "label" in data[index]:
                        label = data[index]["label"]
                    else:
                        label = "undefined"

                    # set annotation position
                    pos = sc.get_offsets()[index]
                    annot.xy = pos

                    # set annotation text
                    text = f"{pos}\ntarget: {target}\ncalculated: {value}\nlabel: {label}\n"

                    annot.set_text(text)
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
                    x = plot_targets[index]["x"]
                    y = plot_targets[index]["y"]
                    if "value" in data[index]:
                        sol = data[index]["value"]
                    else:
                        sol = -1

                    self.lblX["text"] = "{:.4f}".format(x)
                    self.lblY["text"] = "{:.4f}".format(y)
                    self.entInputSol.delete(0, "end")
                    self.entInputSol.insert(0, "{:.4f}".format(sol))
                    self.selected_node_index = index
                    self.plot(plot_targets, data, aggregation_function, l, r)

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
