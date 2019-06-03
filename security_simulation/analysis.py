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
        data = state_dict
        filename = 'SecuritySimulationData_' + str(time.time()) + '.json'

        with open(filename, 'w') as f:
            for chunk in json.JSONEncoder().iterencode(data):
                f.write(chunk)

        return filename

    def load_simulation_file(self, filename):
        """
        Load json file containing simulation data as a dict
        :param filename: name of simulation file to read
        :return: dict of file contents
        """
        data = None
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        return data
