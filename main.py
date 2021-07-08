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
    """ Open a CSV file to return the contained information.

    :return: the data, the bounds and the keys (attributes)
    """
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


def findMostOfParameter(filename):
    """ Finds possible solutions for most-of quantifier and writes them to a file
        Note: this method works only with heart_cleveland dataset and defines a variation of
                accuracy as described in the readme.
    :return:
    """
    target_key = "num"
    keys = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    data, bounds, _ = open_file(filename)
    normalized_data = Model.normalize_input_data(data, bounds)

    count = 0
    divisor = 100
    min_hits = open("training_mostof_acc75.csv", "a")
    max_hits = open("training_mostof_acc82.csv", "a")

    for pattern in product([True, False], repeat=len(keys)):
        if True in pattern and False in pattern:
            list_A = [x[1] for x in zip_longest(pattern, keys) if x[0]]
            list_B = [x[1] for x in zip_longest(pattern, keys) if not x[0]]
            #print(f"{list_A} -- {list_B}")

            for m in range(0,100, 1):
                for n in range(m, 101, 1):
                    quantified_data = Model.apply_quantifier_function(normalized_data, list_A, list_B, "most_of", "most_of", m/divisor, n/divisor)

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
                    if accuracy >= 82:
                        max_hits.write(f"list_A: {list_A};"
                              f"list_B: {list_B};"
                              f"m: {m/divisor};"
                              f"n: {n/divisor};"
                              f"accuracy: {accuracy};"
                              f"tp: {tp};"
                              f"tn: {tn};"
                              f"fp: {fp};"
                              f"fn: {fn}\n")
                    elif accuracy >= 75:
                        min_hits.write(f"list_A: {list_A};"
                              f"list_B: {list_B};"
                              f"m: {m/divisor};"
                              f"n: {n/divisor};"
                              f"accuracy: {accuracy};"
                              f"tp: {tp};"
                              f"tn: {tn};"
                              f"fp: {fp};"
                              f"fn: {fn}\n")

            count += 1
            if count % 100:
                print(f"{datetime.datetime.now()} : {count/8192}")

    print(count)
    max_hits.close()
    min_hits.close()

def evalResults(trainingset, testset):
    """ Checks results of findMostOfParameter() against a testset and prints the results to stdout
        Note: this method works only with heart_cleveland dataset and defines a variation of
                accuracy as described in the readme.
    :return:
    """
    test_set, bounds, _ = open_file(testset)
    normalized_test_set = Model.normalize_input_data(test_set, bounds)

    with open(trainingset, "r") as input_file:
        file = input_file.readlines()
        for line in file:
            splitter = line.replace(" ", "").split(";")
            acc = float(splitter[4].replace("accuracy:", ""))
            if acc > 82:
                list_a = splitter[0].replace("list_A:[", "").replace("]", "").replace("'", "").split(",")
                list_b = splitter[1].replace("list_B:[", "").replace("]", "").replace("'", "").split(",")
                m = float(splitter[2].replace("m:", ""))
                n = float(splitter[3].replace("n:", ""))

                quantified_data = Model.apply_quantifier_function(normalized_test_set, list_a, list_b, "most_of", "most_of",
                                                                  m, n)

                tp = 0
                fp = 0
                tn = 0
                fn = 0
                for i, point in enumerate(quantified_data):
                    if test_set[i]["num"] > 0:
                        if point['x'] + point['y'] >= 1.0:
                            tp += 1
                        else:
                            fn += 1
                    else:
                        if point['x'] + point['y'] >= 1.0:
                            fp += 1
                        else:
                            tn += 1

                accuracy = (tp + tn) / len(quantified_data) * 100
                print(f"list_A: {list_a},"
                       f"list_B: {list_b},"
                       f"m: {m},"
                       f"n: {n},"
                       f"accuracy: {accuracy},"
                       f"tp: {tp},"
                       f"tn: {tn},"
                       f"fp: {fp},"
                       f"fn: {fn}\n")
    pass

if __name__ == "__main__":
    """ Program can be called in 3 ways:
        1. "python main.py" -> opens the interactive ui
        2. "python main.py heart_cleveland.csv" -> aims to find best parameters for most-of quantifier
        3. "python main.py  training_mostof_acc82.csv heart_cleveland_testset.csv" -> validates the results from option 2 
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "eval":
            evalResults(sys.argv[2], sys.argv[3])
        else:
            findMostOfParameter(sys.argv[1])
    else:
        main()
