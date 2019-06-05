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
    def get_wait_times(final_state_dict):
        """
        gets wait times for attendees in a simulation
        must be run on full data
        :param final_state_dict: state_dict of the final time step of a simulation
        :return: tuple(avg, min, max)
        """
        wait_time = [1] * len(final_state_dict.get('attendees'))
        i = 0
        for v in final_state_dict.get('attendees'):
            wait_time[i] = v['total_wait']
            i += 1

        return wait_time

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
    def plot_results(results_file_name, title, x_label):
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
            fig, ax = plt.subplots()
            ax.plot(range(1, (len(data)+1)), minimum, color='blue', label='min')
            ax.plot(range(1, (len(data)+1)), maximum, color='red', label='max')
            ax.plot(range(1, (len(data)+1)), average, color='orange', label='avg')
            plt.xlabel(x_label)
            plt.ylabel("Time(s)")
            plt.title(title)
            legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large')
            legend.get_frame().set_facecolor('C7')
            plt.show()

    @staticmethod
    def wait_time_histogram(num_runs=5, title='Wait Time Histogram', bins=30):
        wait_times = []
        for i in range(num_runs):
            simulation_file = run_sim_from_file('input_parameters.txt').last_sim_filename
            with open(simulation_file, 'r') as file:
                data = json.loads(file.read())
                params = data['params']
                key = params['closed_door_time']
                last_time_step_data = data[str(key)]
                wait_times += Analysis.get_wait_times(last_time_step_data)
        plt.hist(wait_times, bins)
        plt.title(title + " num_attendees=" + str(len(wait_times)/num_runs) + ', num_runs=' + str(num_runs) + ',\n average_time=' + str(N.average(wait_times)))
        plt.show()


# example plotting sensitivity to num attendees
# Analysis.plot_results(Analysis.sensitivity_test('input_parameters.txt',
#                                                 'ATTENDEE_NUMBER',
#                                                 [5000 * i for i in range(1,5)],
#                                                 'attendees',
#                                                 'total_wait',
#                                                 num_steps=4),
#                       'Wait Time Based on Number of Attendees * 5000',
#                       'Number of Attendees * 5000')

# index 0 refers to num of security for bag check
# index 1 refers to num security in metal detector
# index 2 refers num of security after detector
# [1,1,1]
#
# Analysis.plot_results(Analysis.sensitivity_test('input_parameters.txt',
#                                                 'SECURITY_PERSONNEL_SETS',
#                                                 [[[2,10,1]]],
#                                                 'attendees',
#                                                 'total_wait',
#                                                 num_steps=1),
#                       'Wait Time Based on Bag Checkers with 10 metal detectors',
#                       'Number of bag checkers')

Analysis.wait_time_histogram()
# Analysis.plot_results(Analysis.sensitivity_test('input_parameters.txt', 'METAL_MEAN', [.1, .2, .3, .4, .5], 'attendee', 'wait_time', num_steps=5))