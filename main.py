import sys
import tkinter.filedialog as tkFile
import tkinter as tk
import numpy as np
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import os.path as path


# Trash code
class MyView:

    def __init__(self):
        self.data = []

        self.root = tk.Tk()
        # Input
        self.containerInput = tk.Frame(master=self.root, bg="blue")
        self.containerInput.pack(fill=tk.BOTH, side=tk.LEFT)

        self.p = tk.Label(master=self.containerInput, text="hello motherfucker")
        self.p.pack()

        self.btnPlot = tk.Button(master=self.containerInput, text="Plot", command=lambda: self.plot("sell", "time", extreme_x={"min": 400, "max": 600}, extreme_y={"min": 8, "max": 12}, inverse_y=True))
        self.btnPlot.pack()

        # Plot
        self.containerPlot = tk.Frame(master=self.root, bg="red")
        self.containerPlot.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.i = tk.Label(master=self.containerPlot, text="Plot shit here")
        self.i.pack()

        self.figurePlot = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.targetSubPlot = self.figurePlot.add_subplot(111)

        self.canvasPlot = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.figurePlot, master=self.containerPlot)
        self.canvasPlot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.open_file()

    def plot(self, x_key: str, y_key: str, extreme_x={}, extreme_y={}, inverse_x=False, inverse_y=False):

        plot_targets = []

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

        if max_x > extreme_x["max"]:
            max_x = extreme_x["max"]
        if min_x < extreme_x["min"]:
            min_x = extreme_x["min"]
        if max_y > extreme_y["max"]:
            max_y = extreme_y["max"]
        if min_y < extreme_y["min"]:
            min_y = extreme_y["min"]

        # apply min_max_normalization
        for val in self.data:
            x_val = val[x_key]
            if x_val > extreme_x["max"]:
                x_val = extreme_x["max"]
            elif x_val < extreme_x["min"]:
                x_val = extreme_x["min"]

            y_val = val[y_key]
            if y_val > extreme_y["max"]:
                y_val = extreme_y["max"]
            elif y_val < extreme_y["min"]:
                y_val = extreme_y["min"]

            target_x = (x_val - min_x)/(max_x - min_x)
            target_y = (y_val - min_y)/(max_y - min_y)

            if inverse_x:
                target_x = 1 - target_x
            if inverse_y:
                target_y = 1 - target_y

            plot_targets.append({"x": target_x, "y": target_y})
            self.targetSubPlot.scatter(target_x, target_y)

        self.targetSubPlot.set_xlim(0, 1)
        self.targetSubPlot.set_ylim(0, 1)
        # self.targetSubPlot.set_xlim(-0.05, 1.05)
        # self.targetSubPlot.set_ylim(-0.05, 1.05)
        # self.targetSubPlot.set_xticks(10)
        # self.targetSubPlot.set_yticks(10)
        self.targetSubPlot.plot([0.5, 1], [1, 0.5], color='green', linestyle='dotted', linewidth=2)
        self.targetSubPlot.plot([0, 0.5], [0.5, 0], color='green', linestyle='dotted', linewidth=2)
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
            self.p.config(text="File not found!")
            return False

        # self.p.config(text=path.basename(filepath))
        self.p["text"] = path.basename(filepath)

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
