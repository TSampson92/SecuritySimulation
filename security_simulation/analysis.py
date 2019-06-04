import numpy as N
import time
import json
import numpy


class Analysis:
    def __init__(self):
        self.data = {}

    def add_time_step(self, time_step, attendee_list, checkpoint_list,
                      entered_event_list, include_attendees=True,
                      include_checkpoints=False, include_entered=False, minimal=True):
        """
        Add state of current time_step to analysis data
        :param time_step: current simulation time step
        :param attendee_list: list of all attendees
        :param checkpoint_list: list of all checkpoints
        :param entered_event_list: list of attendees that have entered the event
        :return:
        """
        self.data[str(time_step)] = self.state_to_dict(attendee_list, checkpoint_list,
                                                       entered_event_list,
                                                       include_attendees=include_attendees,
                                                       include_checkpoints=include_checkpoints,
                                                       include_entered=include_entered, minimal=minimal)

    def init_sim_data(self, params, checkpoint_list):
        checkpoint_json_list = []
        for checkpoint in checkpoint_list:
            checkpoint_json_list.append(checkpoint.to_dict())
        self.data['checkpoints'] = checkpoint_json_list
        self.data['params'] = params

    def state_to_dict(self, attendee_list, checkpoint_list, entered_event_list,
                      include_attendees=True, include_checkpoints=False,
                      include_entered=False, minimal=True):
        """
        Convert simulations current state to dictionary
        :param attendee_list: list of all attendees
        :param checkpoint_list: list of all checkpoints
        :param entered_event_list: list of attendees that have entered the event
        :return: dict
        """
        data = {}
        attendee_json_list = []
        checkpoint_json_list = []
        entered_event_json_list = []
        if minimal:
            if include_attendees:
                for attendee in attendee_list:
                    attendee_json_list.append(attendee.to_min_dict())
                data['attendees'] = attendee_json_list

            if include_checkpoints:
                for checkpoint in checkpoint_list:
                    checkpoint_json_list.append(checkpoint.to_min_dict())
                data['checkpoints'] = checkpoint_json_list
            if include_entered:
                for attendee in entered_event_list:
                    checkpoint_json_list.append(attendee.to_min_dict())
                data['entered_event'] = entered_event_json_list

        else:
            if include_attendees:
                for attendee in attendee_list:
                    attendee_json_list.append(attendee.to_dict())
                data['attendees'] = attendee_json_list

            if include_checkpoints:
                for checkpoint in checkpoint_list:
                    checkpoint_json_list.append(checkpoint.to_dict())
                data['checkpoints'] = checkpoint_json_list
            if include_entered:
                for attendee in entered_event_list:
                    checkpoint_json_list.append(attendee.to_dict())
                data['entered_event'] = entered_event_json_list

        return data

    def dump_simulation_to_file(self):
        """
        Save all currently stored simulation data to file
        :return: filename
        """
        return self.state_to_json_file(self.data)

    def state_to_json_file(self, state_dict):
        """
        Save a dictionary containing simulation state to file
        :param state_dict:
        :return: filename
        """
        filename = 'SecuritySimulationData_' + str(time.time()) + '.json'
        print('saving simulation data to: %s' % filename)

        # if show_progress:  # slower
        #     state_dict = list(json.JSONEncoder().iterencode(state_dict))
        #     five_percent = len(state_dict)//20
        #     count = 0
        #     with open(filename, 'w') as file:
        #         for chunk in state_dict:
        #             file.write(chunk)
        #             if count % five_percent == 0:
        #                 print(str((count//five_percent) * 5) + '%, ', end='')
        #             count += 1
        # else:

        with open(filename, 'w') as file:
            for chunk in json.JSONEncoder().iterencode(state_dict):
                file.write(chunk)

        return filename

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

    def sensitivity_test_wait_time(self, base_config_filename, attribute_to_adjust_name, values_list, num_steps=10):
        pass
