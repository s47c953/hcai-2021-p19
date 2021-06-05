import tkinter.filedialog as tkFile
import tkinter.ttk
import tkinter as tk
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import numpy

from AxisQueryView import AxisQueryView


class View:

    btn_width = 10

    def __init__(self):

        self.selected_node_index = None

        self.root = tk.Tk()
        self.root.title("Project 19")
        self.root.geometry("800x600")

        # IDs of eventhandle, needed to be unregistered on new plot
        self.hoover_cid = None
        self.click_cid = None

        # Input
        self.containerInput = tk.Frame(master=self.root, width=150)

        # file loading elements
        self.txtFileName = tk.Label(master=self.containerInput, text="File Name")
        self.btnLoadFile = tk.Button(master=self.containerInput,
                                     text="Load File",
                                     width=self.btn_width)
        self.btnLoadFile.pack()
        self.txtFileName.pack()

        # Set keys
        self.aqView = AxisQueryView()
        self.btnQueryWindow = tk.Button(master=self.containerInput,
                                        text="Query",
                                        width=self.btn_width)
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
                                   width=self.btn_width)
        self.btnCalcLR.pack()

        # plotting trigger button
        self.btnPlot = tk.Button(master=self.containerInput,
                                 text="Plot",
                                 width=self.btn_width)
        self.btnPlot.pack()

        # clear data trigger button
        self.btnClear = tk.Button(master=self.containerInput,
                                  text="Clear",
                                  width=self.btn_width)
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
                                     width=self.btn_width)

        self.btnChangeValue = tk.Button(master=self.containerInput,
                                        text="Change",
                                        width=self.btn_width)
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

    def run(self):
        self.root.mainloop()

    def plot(self, plot_targets: [], data: [], raw_data: [], aggregation_function, l, r):
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
                    if "label" in raw_data[index]:
                        label = raw_data[index]["label"]
                    else:
                        label = "undefined"

                    # set annotation position
                    pos = sc.get_offsets()[index]
                    annot.xy = pos

                    # set annotation text
                    text = f"{pos}\ntarget: {target}\ncalculated: {value}\n"
                    for key in raw_data[index]:
                        text += f"{key}: {raw_data[index][key]}\n"

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

                    self.entInputX.delete(0, "end")
                    self.entInputX.insert(0, "{:.4f}".format(x))
                    self.entInputY.delete(0, "end")
                    self.entInputY.insert(0, "{:.4f}".format(y))
                    self.entInputSol.delete(0, "end")
                    self.entInputSol.insert(0, "{:.4f}".format(sol))
                    self.selected_index = index
                    self.plot(plot_targets, data, raw_data, aggregation_function)

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
