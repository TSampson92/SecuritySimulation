import os
import json
import numpy as N
from security_simulation.Main import run_sim_from_file
import time
import matplotlib.pyplot as plt

class Analysis:
    from security_simulation.Main import run_sim_from_file
    def load_simulation_file(filename):
        """
        Load json file containing simulation data as a dict
        :param filename: name of simulation file to read
        :return: dict of file contents
        """
        data = None
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        return data

    @staticmethod
    def avg_min_max_wait_time(final_state_dict, object_name, variable_name):
        """
        calulates average, minimum, and maximum wait times for attendees
        must be run on full data
        :param final_state_dict: state_dict of the final time step of a simulation
        :return: tuple(avg, min, max)
        """
        wait_time = N.ones(len(final_state_dict.get(object_name)))
        i = 0
        for v in final_state_dict.get(object_name):
            wait_time[i] = v[variable_name]
            i += 1

        return N.average(wait_time), N.min(wait_time), N.max(wait_time)

    @staticmethod
    def sensitivity_test(base_config_filename,
                         attribute_to_adjust_name, 
                         values_list, 
                         object_name, 
                         variable_name, 
                         num_steps=3):
        """
        Runs multiple simulations varying one parameter producing a results file
        e.g. Analysis.sensitivity_test('input_parameters.txt', 'METAL_MEAN', [.1, .2, .3, .4, .5], num_steps=5)
        :param base_config_filename: path to file of the base config file to use
        :param attribute_to_adjust_name: name of attribute being varied in the config file
        :param values_list: list containing all the values fo the attribute_to_adjust that will be used
        :param num_steps:  number of simulations to run, needs to be same length as values list
        :return: filename of results file. results file is a json file that contains a dictionary with the keys "0" to
                 num_steps, each key representing one simulation. key "0" is the simulation using the value in
                 values_list[0].
        """
        loaded_config_data = None
        
        directory_path = os.path.realpath(os.path.join(os.getcwd(), 
                                          os.path.dirname(__file__)))

        input_file_path = os.path.join(directory_path, base_config_filename)

        with open(input_file_path, 'r') as file:
            loaded_config_data = json.loads(file.read())

        # generate needed config files
        config_file_names = []
        for i in range(num_steps):
            directory_path = os.path.realpath(os.path.join(os.getcwd(), 
                                          os.path.dirname(__file__)))

            new_config_name = os.path.join(directory_path, 
                                           'sensitivity_config_' 
                                           + str(time.time()) 
                                           + '_' 
                                           + str(i))
            loaded_config_data[attribute_to_adjust_name] = values_list[i]
            with open(new_config_name, 'w') as file:
                file.write(json.dumps(loaded_config_data))
            config_file_names.append(new_config_name)

        # run a simulation for each config file
        sim_data_file_names = []
        for name in config_file_names:
            sim_data_file_names.append(run_sim_from_file(name).last_sim_filename)

        # analyze data from simulations to get min, max, avg
        results = {}
        i = 0
        for name in sim_data_file_names:
            sim_data = Analysis.load_simulation_file(name)
            params = sim_data['params']
            last_time_step = str(params['closed_door_time'])
            results[str(i)] = Analysis.avg_min_max_wait_time(sim_data[last_time_step], object_name, variable_name)
            i += 1

        # write the results to file
        results_file_name = 'sensitivity_results_' + str(time.time())
        with open (results_file_name, 'w') as file:
            file.write(json.dumps(results))
        return results_file_name

    @staticmethod
    def plot_results(results_file_name):
        """
        plots avg, min, max from sensitivity analysis
        :param results_file_name: filename from output of sensitivity_test
        :return:
        """
        with open(results_file_name, 'r') as file:
            data = json.loads(file.read())
            average = []
            minimum = []
            maximum = []
            for i in range(len(data)):
                results = data[str(i)]
                average.append(results[0])
                minimum.append(results[1])
                maximum.append(results[2])
            plt.plot(range(0, (len(data))), minimum, color='blue')
            plt.plot(range(0, (len(data))), maximum, color='red')
            plt.plot(range(0, (len(data))), average, color='orange')
            plt.show()


# example plotting sensitivity to num attendees
Analysis.plot_results(Analysis.sensitivity_test('input_parameters.txt', 'ATTENDEE_NUMBER', [5 * i for i in range(1,26)], 'attendees', 'wait_time', num_steps=25))
# Analysis.plot_results(Analysis.sensitivity_test('input_parameters.txt', 'METAL_MEAN', [.1, .2, .3, .4, .5], 'attendee', 'wait_time', num_steps=5))