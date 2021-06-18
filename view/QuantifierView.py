import tkinter as tk

AXIS_X = "x"
AXIS_Y = "y"

MODE_CONJUNCTION = "conjunction"
MODE_DISJUNCTION = "disjunction"
MODE_MOST_OF = "most_of"


class QuantifierView:
    btn_sign_width = 3
    btn_text_width = 10

    queryWindow: tk.Toplevel
    entry_m: tk.Entry
    entry_n: tk.Entry

    def __init__(self):
        self.axisSelection = tk.StringVar()
        self.modeSelection = tk.StringVar()
        self.key_selection = {str: tk.IntVar}
        self.x_mode = None
        self.y_mode = None
        self.keys_x = []
        self.keys_y = []
        self.m = 0.0
        self.n = 0.0

        pass

    def create_axis_inputs(self):
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

    def create_mode_inputs(self):
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
                                value=MODE_MOST_OF)

        label_mode = tk.Label(master=container_modes,
                              text="Mode:",
                              font=("Arial", 14))

        label_mode.grid(row=0, column=0)
        conjunction.grid(row=0, column=1)
        disjunction.grid(row=0, column=2)
        mostof.grid(row=0, column=3)

        container_modes.pack(fill=tk.X)

    def create_key_entries(self, keys: []):
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

        container_keys.pack(fill=tk.X)

    def create_control_inputs(self, keys):

        label_y_axis = tk.Label(self.queryWindow,
                                text="Selection:",
                                font=("Arial", 14))
        label_y_axis.pack()

        str_x_axis = "X-Axis: "
        label_x_axis = tk.Label(self.queryWindow, text=str_x_axis)
        label_x_axis.pack()

        str_y_axis = "Y-Axis: "
        label_y_axis = tk.Label(self.queryWindow, text=str_y_axis)
        label_y_axis.pack()

        def apply():
            axis = self.axisSelection.get()
            mode = self.modeSelection.get()
            selected_keys = []
            for key in keys:
                if self.key_selection[key].get() == 1:
                    selected_keys.append(key)

                self.key_selection[key].set(0)

            if axis == AXIS_X:
                self.keys_x = selected_keys
                self.x_mode = mode
                label_x_axis["text"] = str_x_axis + "mode = " + mode + "; keys = " + str(selected_keys)
            else:
                self.keys_y = selected_keys
                self.y_mode = mode
                label_y_axis["text"] = str_y_axis + "mode = " + mode + "; keys = " + str(selected_keys)

            if self.entry_m.get() != "":
                self.m = float(self.entry_m.get())

            if self.entry_n.get() != "":
                self.n = float(self.entry_n.get())

        def close():
            self.queryWindow.destroy()

        test = tk.Button(self.queryWindow,
                         text="Apply for Axis",
                         command=apply)
        test.pack()

        test = tk.Button(self.queryWindow,
                         text="Save and Close",
                         command=close)
        test.pack()

    def create_most_of_controls(self):
        container_most_of = tk.Frame(self.queryWindow)
        container_most_of.rowconfigure(0)
        container_most_of.columnconfigure(0)

        label_y_axis = tk.Label(container_most_of, text="m:")
        label_y_axis.grid(row=0, column=0)
        self.entry_m = tk.Entry(container_most_of)
        self.entry_m.grid(row=0, column=1)

        label_y_axis = tk.Label(container_most_of, text="n:")
        label_y_axis.grid(row=1, column=0)
        self.entry_n = tk.Entry(container_most_of)
        self.entry_n.grid(row=1, column=1)

        container_most_of.pack(fill=tk.X)

    def open_query_window(self, keys: []):
        # Query Window
        self.queryWindow = tk.Toplevel()
        self.queryWindow.title("Query")
        # self.queryWindow.geometry("400x200")
        self.queryWindow.resizable(width=False, height=False)

        self.create_axis_inputs()
        self.create_mode_inputs()
        self.create_most_of_controls()
        self.create_key_entries(keys)
        self.create_control_inputs(keys)
