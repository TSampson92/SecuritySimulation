import numpy as N
import time
import json


class Analysis:
    def __init__(self):
        self.data = {}

    def add_time_step(self, time_step, attendee_list, checkpoint_list, entered_event_list):
        """
        Add state of current time_step to analysis data
        :param time_step: current simulation time step
        :param attendee_list: list of all attendees
        :param checkpoint_list: list of all checkpoints
        :param entered_event_list: list of attendees that have entered the event
        :return:
        """
        self.data[str(time_step)] = self.state_to_dict(attendee_list, checkpoint_list, entered_event_list)

    def state_to_dict(self, attendee_list, checkpoint_list, entered_event_list):
        """
        Convert simulations current state to dictionary
        :param attendee_list: list of all attendees
        :param checkpoint_list: list of all checkpoints
        :param entered_event_list: list of attendees that have entered the event
        :return: dict
        """
        attendee_json_list = []
        checkpoint_json_list = []
        entered_event_json_list = []
        for attendee in attendee_list:
            attendee_json_list.append(attendee.to_dict())
        for checkpoint in checkpoint_list:
            checkpoint_json_list.append(checkpoint.to_dict())
        for attendee in entered_event_list:
            checkpoint_json_list.append(attendee.to_dict())
        data = {'attendees': attendee_json_list,
                'checkpoints': checkpoint_json_list,
                'entered_event': entered_event_json_list}
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
