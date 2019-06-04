import json
import numpy as N
from security_simulation.Main import run_sim_from_file
import time

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
    def avg_min_max_wait_time(final_state_dict):
        """
        calulates average, minimum, and maximum wait times for attendees
        must be run on full data
        :param final_state_dict: state_dict of the final time step of a simulation
        :return: tuple(avg, min, max)
        """
        wait_time = N.ones(len(final_state_dict.get('attendees')))
        i = 0
        for v in final_state_dict.get('attendees'):
            wait_time[i] = v['total_wait']
            i += 1

        return N.average(wait_time), N.min(wait_time), N.max(wait_time)

    @staticmethod
    def sensitivity_test_wait_time(base_config_filename, attribute_to_adjust_name, values_list, num_steps=3):
        base_config_data = None
        with open(base_config_filename, 'r') as file:
            base_config_data = json.loads(file.read())

        config_file_names = []
        for i in range(num_steps):
            new_cofig_name = 'sensitivity_config_' + str(time.time()) + '_' + str(i)
            base_config_data[attribute_to_adjust_name] = values_list[i]
            with open(new_cofig_name, 'w') as file:
                file.write(json.dumps(base_config_data))
            config_file_names.append(new_cofig_name)

        sim_data_file_names = []
        for name in config_file_names:
            sim_data_file_names.append(run_sim_from_file(name).last_sim_filename)
        results = {}
        i = 0
        for name in sim_data_file_names:
            sim_data = Analysis.load_simulation_file(name)
            params = sim_data['params']
            last_time_step = str(params['closed_door_time'])
            results[str(i)] = Analysis.avg_min_max_wait_time(sim_data[last_time_step])
            i += 1

        results_file_name = 'sensitivity_results_' + str(time.time())
        with open (results_file_name, 'w') as file:
            file.write(json.dumps(results))
        return results_file_name


# Analysis.sensitivity_test_wait_time('input_parameters.txt', 'ATTENDEE_NUMBER', [10, 20, 30, 40], num_steps=4)
