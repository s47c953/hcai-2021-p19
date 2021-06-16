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


def open_file() -> (str, [], {}, []):

    """Open a file for editing."""
    filepath = tkFile.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    # Should not be possible:
    if not filepath:
        return "File not found!", None, None, None

    label_text = "File Name: " + path.basename(filepath)

    result = []
    with open(filepath, "r") as input_file:
        file = input_file.readlines()

        keys: []
        bounds: {}

        for lineNr, line in enumerate(file):

            if lineNr == 0:
                entries = line.replace("\n", "").split(",")
                keys = entries
                continue

            entries = line.replace(" ", "").replace("\n", "").split(",")
            if lineNr == 1:
                bounds = parseBoundaries(keys, entries)
                continue

            value_dict = {}

            for index, entry in enumerate(entries):
                try:
                    value_dict[keys[index]] = float(entry.strip())
                except:
                    value_dict[keys[index]] = entry.strip()

            result.append(value_dict)

    return label_text, result, bounds, keys
