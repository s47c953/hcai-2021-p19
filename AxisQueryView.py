import tkinter as tk

AXIS_X = "x"
AXIS_Y = "y"

MODE_CONJUNCTION = "conjunction"
MODE_DISJUNCTION = "disjunction"
MODE_MOSTOF = "mostof"


class AxisQueryView:
    btn_sign_width = 3
    btn_text_width = 10

    queryWindow: tk.Toplevel

    def __init__(self):
        self.axisSelection = tk.StringVar()
        self.modeSelection = tk.StringVar()
        pass

    def createAxisInputs(self):
        container_axis = tk.Frame(master=self.queryWindow, width=150)
        container_axis.rowconfigure(0, minsize=50)
        container_axis.columnconfigure(0, minsize=50)

        x_axis = tk.Radiobutton(container_axis,
                                text="X",
                                variable=self.axisSelection,
                                value=AXIS_X)
        y_axis = tk.Radiobutton(container_axis,
                                text="Y",
                                variable=self.axisSelection,
                                value=AXIS_Y)

        label_axis = tk.Label(master=container_axis,
                              text="Axis:",
                              font=("Arial", 14))

        label_axis.grid(row=0, column=0)
        x_axis.grid(row=0, column=1)
        y_axis.grid(row=0, column=2)

        container_axis.pack(fill=tk.X)

    def createModeInputs(self):
        container_modes = tk.Frame(master=self.queryWindow, width=150)
        container_modes.rowconfigure(0, minsize=50)
        container_modes.columnconfigure(0, minsize=50)

        # Button variant
        # conjunction = tk.Button(master=self.containerInput,
        #                                 text="⋀",
        #                                 width=self.btn_sign_width)
        #
        # disjunction = tk.Button(master=self.containerInput,
        #                                 text="⋁",
        #                                 width=self.btn_sign_width)
        #
        # mostof = tk.Button(master=self.containerInput,
        #                            text="mostOf",
        #                            width=self.btn_text_width)

        # Radio Button variant
        conjunction = tk.Radiobutton(container_modes,
                                     text="⋀",
                                     variable=self.modeSelection,
                                     value=MODE_CONJUNCTION)
        disjunction = tk.Radiobutton(container_modes,
                                     text="⋁",
                                     variable=self.modeSelection,
                                     value=MODE_DISJUNCTION)
        mostof = tk.Radiobutton(container_modes,
                                text="MostOf",
                                variable=self.modeSelection,
                                value=MODE_MOSTOF)

        label_mode = tk.Label(master=container_modes,
                              text="Mode:",
                              font=("Arial", 14))

        label_mode.grid(row=0, column=0)
        conjunction.grid(row=0, column=1)
        disjunction.grid(row=0, column=2)
        mostof.grid(row=0, column=3)

        container_modes.pack(fill=tk.X)

    def open_query_window(self, keys: []):
        # Query Window
        self.queryWindow = tk.Toplevel()
        self.queryWindow.title("Query")
        self.queryWindow.geometry("300x150")

        self.createAxisInputs()
        self.createModeInputs()

        def test_btn():
            self.label_testAxis["text"] = self.axisSelection.get()
            self.label_testMode["text"] = self.modeSelection.get()

        test = tk.Button(self.queryWindow,
                         text="test",
                         width=self.btn_sign_width,
                         command=test_btn)
        test.pack()

        self.label_testAxis = tk.Label(self.queryWindow)
        self.label_testAxis.pack()
        self.label_testMode = tk.Label(self.queryWindow)
        self.label_testMode.pack()
