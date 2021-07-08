import time

from model.Model import Model
from model.Filehandler import open_file
from view.View import View

class Controller:
    """Controller Class
    The controller of the MVC application.
    """

    def __init__(self, model: Model, view: View):
        """ Constructor
        Initialising of variables for the loaded data and registering of event handlers.

        :param model: The Model.
        :param view: The View.
        """

        # MVC classes
        self.model = model
        self.view = view

        # object to keep track of loaded data
        self.raw_data = None
        self.normalized_data = None
        self.quantified_data = None
        self.keys = None
        self.bounds = None
        self.target_values = {}

        # register event handler
        self.view.register_load_file_event(self.load_file)
        self.view.register_clear_event(self.clear_data)
        self.view.register_quantifier_button_event(lambda: self.view.quantifier_view_wrapper(self.keys))
        self.view.register_plot_event(self.plot_data)
        self.view.register_calc_l_r_event(self.calculate_lambda_r)
        self.view.register_set_value_event(self.change_target_value)

    def load_file(self):
        """ Loads the CSV file and sets all the gathered data.

        :return: void
        """
        label_string, data, bounds, keys = open_file()
        if not data:
            return
        self.view.set_label_file_text(label_string)
        normalized_data = self.model.normalize_input_data(data, bounds)
        self.raw_data = data
        self.normalized_data = normalized_data
        self.keys = keys
        self.bounds = bounds

    def clear_data(self):
        """ Clears the loaded data.

        :return: void
        """
        self.raw_data = None
        self.normalized_data = None
        self.quantified_data = None
        self.keys = None
        self.bounds = None
        self.target_values = {}
        self.calculate_lambda_r()
        self.plot_data()

    def plot_data(self):
        """ Plots the set data.

        :return: void
        """

        # get data for applying quantifier functions
        x_keys, y_keys = self.view.get_quantifier_axes()
        x_mode, y_mode = self.view.get_quantifier_modes()
        m, n = self.view.get_quantifier_m_n()

        # l, r = self.view.get_lambda_r()
        # selected_aggregation_function = self.view.get_selected_aggregation_function()
        # aggregation_function = self.model.get_aggregation_function_from_string(selected_aggregation_function)
        # start = time.time()
        # self.quantified_data = self.model.apply_quantifier_function(self.normalized_data, x_keys, y_keys, x_mode, y_mode, m,
        #                                                             n)
        # end = time.time()
        #
        # cps = 1 / (end - start)
        # print(f"calcs per sec: {cps}")


        self.quantified_data = self.model.apply_quantifier_function(self.normalized_data, x_keys, y_keys, x_mode, y_mode, m, n)
        self.quantified_data = self.model.restore_target_values(self.quantified_data, self.target_values)
        if "num" in self.raw_data[0]:
            # case only happens in heart_cleveland dataset. automatically labels target values in respect to diagnosis
            self.quantified_data = self.model.restore_target_values(self.quantified_data, None, self.raw_data)
        else:
            self.quantified_data = self.model.restore_target_values(self.quantified_data, self.target_values)


        # get aggregation parameter
        l, r = self.view.get_lambda_r()
        selected_aggregation_function = self.view.get_selected_aggregation_function()
        aggregation_function = self.model.get_aggregation_function_from_string(selected_aggregation_function)

        plot_targets, value_sum = self.model.prepare_plot_targets(self.quantified_data, aggregation_function, l, r)
        self.view.set_sum_value(value_sum)
        self.view.plot(plot_targets, self.quantified_data, self.raw_data, aggregation_function, l, r)

    def change_target_value(self):
        """ Changes the target value of a node.

        :return: void
        """
        selected_node = self.view.get_selected_note_index()
        target_value = self.view.get_target_node_value()
        self.target_values[selected_node] = target_value
        self.quantified_data[selected_node]["value"] = target_value

    def calculate_lambda_r(self):
        """ Calculates lambda and r from the loaded data.

        :return: void
        """
        selected_aggregation_function = self.view.get_selected_aggregation_function()
        aggregation_function = self.model.get_aggregation_function_from_string(selected_aggregation_function)
        l_mean, r_mean, l, r = aggregation_function.get_lambda_r(self.quantified_data, 0.0001, 4.0, 0.0001, 5.0, 0.0001)
        self.view.set_lambda_r(l, r, l_mean, r_mean)
