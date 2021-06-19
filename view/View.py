import tkinter as tk
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import numpy
from PIL import Image

from view.QuantifierView import QuantifierView


class View:
    """View Class
    This class is the View in our MVC application.
    It contains the main window generation as well as all the events and functions for UI manipulation.
    """

    # UI constants
    BUTTON_WIDTH = 10

    def __init__(self):
        """ Constructor
        The main window with all the containers and inputs is generated here.
        """

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
        self.txtFileName = tk.Label(master=self.containerInput, text="No File")
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
        choices = {'Lukasiewicz', 'MinMax', 'TnormTconormGeometric', 'TnormTconormArithmetic'}
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
        self.entL = tk.Entry(master=self.gridLambdaR, width=6)
        self.entL.insert(0, 1.0)
        self.entL.grid(row=0, column=1)
        self.entR = tk.Entry(master=self.gridLambdaR, width=6)
        self.entR.insert(0, 1.0)
        self.entR.grid(row=1, column=1)
        self.lblErrorL = tk.Label(master=self.gridLambdaR, text="0.0")
        self.lblErrorL.grid(row=2, column=1)
        self.lblErrorR = tk.Label(master=self.gridLambdaR, text="0.0")
        self.lblErrorR.grid(row=3, column=1)
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
        lbl_sum_value = tk.Label(master=self.gridSum, textvariable=self.txtSumValue)
        lbl_sum_value.grid(row=0, column=1)
        self.gridSum.pack(fill=tk.X, anchor=tk.NW)

        # Node Information
        self.nodeInfo = tk.Frame(self.containerInput, width=150)
        tk.Label(self.nodeInfo, text="Node Information", font=("Arial", 11)).pack(anchor=tk.W)
        self.lblNodeInfo = tk.Label(self.nodeInfo, width=145)
        self.lblNodeInfo.pack(anchor=tk.W)
        self.nodeInfo.pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))

        # ContainerInput end
        self.containerInput.pack(fill=tk.Y, side=tk.LEFT)
        self.containerInput.pack_propagate(0)

        # Plot section
        self.containerPlot = tk.Frame(master=self.root)
        self.containerPlot.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.figurePlot = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.targetSubPlot = self.figurePlot.add_subplot(111)
        self.targetSubPlot.set_xticks(numpy.arange(0, 1.1, 0.1))
        self.targetSubPlot.set_yticks(numpy.arange(0, 1.1, 0.1))

        self.canvasPlot = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.figurePlot,
                                                                              master=self.containerPlot)
        self.canvasPlot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def quantifier_view_wrapper(self, keys: list):
        """ Opens the quantifier/query window. 'keys' is the list of attribute names from the data.

        :param keys: The keys from the loaded csv file.
        :return: void
        """
        self.aqView.open_query_window(keys)

    def register_quantifier_button_event(self, event):
        """ Sets the event on the 'Query' button.

        :param event: The event to set.
        :return: void
        """
        self.btnQueryWindow["command"] = event

    def register_load_file_event(self, event):
        """ Sets the event to the 'Load' button.

        :param event: The event to set.
        :return: void
        """
        self.btnLoadFile["command"] = event

    def register_calc_l_r_event(self, event):
        """ Sets the event to the 'calc l r' button.

        :param event: The event to set.
        :return: void
        """
        self.btnCalcLR["command"] = event

    def register_plot_event(self, event):
        """ Sets the event to the 'Plot' button.

        :param event: The event to set.
        :return: void
        """
        self.btnPlot["command"] = event

    def register_clear_event(self, event):
        """ Sets the event to the 'Clear' button.

        :param event: The event to set.
        :return: void
        """
        self.btnClear["command"] = event

    def register_set_value_event(self, event):
        """ Sets the event to the 'Set' button.

        :param event: The event to set.
        :return: void
        """
        self.btnSetValue["command"] = event

    def set_label_file_text(self, text: str):
        """ Sets the text to the 'File Name' label.

        :param text: The filename.
        :return: void
        """
        self.txtFileName["text"] = text

    def set_lambda_r(self, lam: float, r: float, l_error: float, r_error: float):
        """ Empties the lambda and r entries and inserts the new values for lambda.
        Additionally the errors of lambda and r are set to the respective labels.

        :param lam: The value for lambda.
        :param r: The value for r.
        :param l_error: The error of lambda.
        :param r_error: The error of r.
        :return: void
        """
        self.entR.delete(0, "end")
        self.entR.insert(0, "{:.4f}".format(r))
        self.entL.delete(0, "end")
        self.entL.insert(0, "{:.4f}".format(lam))
        self.lblErrorL["text"] = "{:.4f}".format(l_error)
        self.lblErrorR["text"] = "{:.4f}".format(r_error)

    def set_sum_value(self, value: float):
        """ Sets the total sum of all the data points.

        :param value: The value for the sum information.
        :return:  void
        """
        self.txtSumValue.set("{:.4f}".format(value))

    def get_lambda_r(self) -> (float, float):
        """ Returns the current values in the entries for lambda and r.

        :return: The values for lambda and r.
        """
        lam = float(self.entL.get())
        r = float(self.entR.get())
        return lam, r

    def get_quantifier_axes(self) -> (list, list):
        """ Returns the x and y keys (attribute list) which were set in the quantifier/query window.

        :return: The keys for x and y.
        """
        x_keys = self.aqView.keys_x
        y_keys = self.aqView.keys_y
        return x_keys, y_keys

    def get_quantifier_m_n(self) -> (float, float):
        """ Returns m and n of the quantifier/query window.

        :return: The values for m and n.
        """
        m = self.aqView.m
        n = self.aqView.n
        return m, n

    def get_quantifier_modes(self) -> (str, str):
        """ Returns the quantifier mode set in the quantifier/query window.

        :return: The set quantifier modes.
        """
        x_mode = self.aqView.x_mode
        y_mode = self.aqView.y_mode
        return x_mode, y_mode

    def get_selected_aggregation_function(self) -> str:
        """ Returns the aggregation function selected in the dropdown.

        :return: The set aggregation function.
        """
        return self.aggregationPopupValue.get()

    def get_selected_note_index(self) -> int:
        """ Returns the index of the node which is currently selected in the chart.

        :return: The index of the selected node.
        """
        return self.selected_node_index

    def get_target_node_value(self) -> float:
        """ Returns the target value for the node which was entered in the corresponding entry widget.

        :return: The set target value.
        """
        return float(self.entInputSol.get())

    def run(self):
        """ Executes the loop for the UI.

        :return: void
        """
        self.root.mainloop()

    @staticmethod
    def create_background(aggregation_function, lam, r):
        """ Creates the background of the chart out of an array of points generated by using the
        provided aggregation function. This results in a gradient like image from red (low value, 0)
        to green (high value, 1) depending on the value of the datapoint in each location.

        :param aggregation_function: The  selected aggregation function.
        :param lam: Value of lambda.
        :param r: Value of r.
        :return: The final image according to the aggregation function, lambda and r.
        """

        resolution = 500

        # gradient between 0 and 1 for 256*256
        array = numpy.empty((resolution, resolution, 3), numpy.uint8)

        for y in range(0, resolution):
            for x in range(0, resolution):
                value = aggregation_function.perform(x / resolution, y / resolution, lam, r)
                # add blue color to maybe points
                if value != 0 and value != 1:
                    blue_val = 44
                else:
                    blue_val = 00

                red_val = 255 - int(255 * value)
                green_val = int(255 * value)
                array[resolution - y - 1][x] = [red_val, green_val, blue_val]

        # Creates PIL image
        img = Image.fromarray(array, 'RGB')
        return img

    def plot(self, plot_targets: [], data: [], raw_data: [], aggregation_function, lam, r):
        """ TODO docu

        :param plot_targets:
        :param data:
        :param raw_data:
        :param aggregation_function:
        :param lam: The value of lambda.
        :param r: The value of r.
        :return:
        """
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
                border_targets.append("blue")
            else:
                border_targets.append("black")

        img = self.create_background(aggregation_function, lam, r)
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

                    annotation_text = ""

                    # set annotation position
                    pos = sc.get_offsets()[index]
                    annot.xy = pos
                    annotation_text += f"{pos}\n"

                    if "value" in data[index]:
                        data_value = data[index]["value"]
                        annotation_text += f"target: {data_value}\n"
                    else:
                        annotation_text += "target: Not defined\n"

                    annotation_text += f"calculated: {value}\n"

                    if "label" in raw_data[index]:
                        data_label = raw_data[index]["label"]
                        annotation_text += f"label: {data_label}"

                    # set annotation text
                    annot.set_text(annotation_text)
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
                    raw_point_data = raw_data[index]
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
                    # self.plot(plot_targets, data, aggregation_function, l, r)

                    # enter node info
                    info = ""
                    for entry in raw_point_data:
                        info += entry + ": "
                        info += str(raw_point_data[entry])
                        info += "\n"
                    self.lblNodeInfo["text"] = info

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
        marker_x_yes, marker_y_yes, marker_x_no, marker_y_no = aggregation_function.get_marker(lam)
        self.targetSubPlot.axhline(y=0.5, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axhline(y=0, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axhline(y=1, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=0.5, color='black', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=0, color='gray', linestyle='dotted', linewidth=1)
        self.targetSubPlot.axvline(x=1, color='gray', linestyle='dotted', linewidth=1)
        # self.targetSubPlot.plot([0, 0.5], [0.5, 0], color='black', linestyle='dotted', linewidth=1)

        # draw yes-no borders
        self.targetSubPlot.plot(marker_x_yes, marker_y_yes, color='black', linestyle='dotted', linewidth=2)
        self.targetSubPlot.plot(marker_x_no, marker_y_no, color='black', linestyle='dotted', linewidth=2)

        # draw the data
        self.canvasPlot.draw()
