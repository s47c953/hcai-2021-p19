from tkinter import Label
import tkinter.filedialog as tkFile
import os.path as path


def parseBoundaries(keys: [str], bounds: [str]) -> {}:
    result = {}
    for i, key in enumerate(keys):
        if key == "value":
            break
        target_bounds = bounds[i].split("|")
        result[key] = {"min": float(target_bounds[0]), "max": float(target_bounds[1])}
    return result


def open_file(text_label: Label) -> (bool, [], {}):

    """Open a file for editing."""
    # source: https://realpython.com/python-gui-tkinter/#building-a-text-editor-example-app
    filepath = tkFile.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    # Should not be possible:
    if not filepath:
        text_label.config(text="File not found!")
        return False, [], {}

    text_label["text"] = "File Name: " + path.basename(filepath)

    result = []
    with open(filepath, "r") as input_file:
        file = input_file.readlines()

        keys: []
        bounds: {}

        for lineNr, line in enumerate(file):
            entries = line.replace(" ", "").replace("\n", "").split(",")

            if lineNr == 0:
                keys = entries
                continue

            if lineNr == 1:
                bounds = parseBoundaries(keys, entries)
                continue

            value_dict = {}

            for index, entry in enumerate(entries):
                value_dict[keys[index]] = float(entry.strip())

            result.append(value_dict)

    return True, result, bounds
