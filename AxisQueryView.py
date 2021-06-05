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
        self.key_selection = {str: tk.IntVar}
        self.keys_x = []
        self.keys_y = []

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

    def createKeyEntries(self, keys: []):
        container_keys = tk.Frame(self.queryWindow, width=150)
        container_keys.rowconfigure(0, minsize=50)
        container_keys.columnconfigure(0, minsize=50)

        label_mode = tk.Label(container_keys,
                              text="Keys:",
                              font=("Arial", 14))
        label_mode.grid(row=0, column=0, sticky=tk.W)

        row = 1
        column = 0
        for key in keys:

            if column == 4:
                row += 1
                column = 0

            key_var = tk.IntVar()
            self.key_selection[key] = key_var

            btn = tk.Checkbutton(container_keys,
                                 text=key,
                                 variable=key_var,
                                 wraplength=150,
                                 onvalue=1,
                                 offvalue=0)
            btn.grid(row=row, column=column, sticky=tk.W)

            column += 1

        container_keys.pack()

    def open_query_window(self, keys: []):
        # Query Window
        self.queryWindow = tk.Toplevel()
        self.queryWindow.title("Query")
        # self.queryWindow.geometry("400x200")
        self.queryWindow.resizable(width=False, height=False)

        self.createAxisInputs()
        self.createModeInputs()
        self.createKeyEntries(keys)

        str_x_axis = "X-Axis: "
        label_x_axis = tk.Label(self.queryWindow, text=str_x_axis)
        label_x_axis.pack()

        str_y_axis = "Y-Axis: "
        label_y_axis = tk.Label(self.queryWindow, text=str_y_axis)
        label_y_axis.pack()

        def test_btn():
            axis = self.axisSelection.get()
            mode = self.modeSelection.get()
            selected_keys = []
            for key in keys:
                if self.key_selection[key].get() == 1:
                    selected_keys.append(key)

            if axis == AXIS_X:
                self.keys_x = selected_keys

                label_x_axis["text"] = str_x_axis + "mode = " + mode + "; keys = " + str(selected_keys)
            else:
                self.keys_y = selected_keys
                label_y_axis["text"] = str_y_axis + "mode = " + mode + "; keys = " + str(selected_keys)

        test = tk.Button(self.queryWindow,
                         text="Apply for Axis",
                         width=self.btn_sign_width,
                         command=test_btn)
        test.pack()
