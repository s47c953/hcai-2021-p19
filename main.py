import sys
import time

from model.Model import Model
from view.View import View
from controller.Controller import Controller
from model.Filehandler import parse_boundaries
from itertools import *
import datetime


def main():
    """ Start point of the application.
    Model, View and Controller are instantiated here and the application started.

    :return: void
    """

    # create MVC
    m = Model()
    v = View()
    Controller(m, v)

    # start application
    v.run()


def open_file(filepath) -> ([], {}, []):

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
                bounds = parse_boundaries(keys, entries)
                continue

            value_dict = {}

            for index, entry in enumerate(entries):
                try:
                    value_dict[keys[index]] = float(entry.strip())
                except:
                    value_dict[keys[index]] = entry.strip()

            result.append(value_dict)

    return result, bounds, keys

def plotResult():
    pass

def bruteForce(filename):
    target_key = "num"
    keys = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    data, bounds, _ = open_file(filename)
    normalized_data = Model.normalize_input_data(data, bounds)

    count = 0
    estimated_counts = 2358720
    target_x = []
    taret_y = []
    min_hits = open("brutal_min.csv", "a")
    max_hits = open("brutal_max.csv", "a")

    for pattern in product([True, False], repeat=len(keys)):
        if True in pattern and False in pattern:
            list_A = [x[1] for x in zip_longest(pattern, keys) if x[0]]
            list_B = [x[1] for x in zip_longest(pattern, keys) if not x[0]]
            #print(f"{list_A} -- {list_B}")

            for m in range(0,10):
                for n in range(m, 11):
                    quantified_data = Model.apply_quantifier_function(normalized_data, list_A, list_B, "most_of", "most_of", m/10, n/10)

                    tp = 0
                    fp = 0
                    tn = 0
                    fn = 0
                    for i, point in enumerate(quantified_data):
                        if data[i][target_key] > 0:
                            if point['x'] + point['y'] >= 1.0:
                                tp+=1
                            else:
                                fn+=1
                        else:
                            if point['x'] + point['y'] >= 1.0:
                                fp+=1
                            else:
                                tn+=1

                    accuracy = (tp+tn)/len(quantified_data)*100
                    if accuracy >= 80:
                        max_hits.write(f"list_A: {list_A},"
                              f"list_B: {list_B},"
                              f"m: {m},"
                              f"n: {n},"
                              f"accuracy: {accuracy},"
                              f"tp: {tp},"
                              f"tn: {tn},"
                              f"fp: {fp},"
                              f"fn: {fn}\n")
                    elif accuracy >= 70:
                        min_hits.write(f"list_A: {list_A},"
                              f"list_B: {list_B},"
                              f"m: {m},"
                              f"n: {n},"
                              f"accuracy: {accuracy},"
                              f"tp: {tp},"
                              f"tn: {tn},"
                              f"fp: {fp},"
                              f"fn: {fn}\n")

            count += 1
            if count % 5000:
                pass #print(f"{datetime.datetime.now()} : {count/estimated_counts}")

    print(count)
    max_hits.close()
    min_hits.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        bruteForce(sys.argv[1])
    else:
        main()
