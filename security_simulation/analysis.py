import numpy as N
import time
import json


def save_to_json(attendee_list):
    """
    Save all attendee data as a json file
    :param attendee_list: list of attendees in simulation
    :return: filename: str
    """
    json_list = []
    for attendee in attendee_list:
        json_list.append(attendee.to_dict())
    data = json.dumps({'attendees': json_list})
    filename = 'SecuritySimulationData_' + str(time.time()) + '.json'
    with open(filename, 'w') as file:
        file.write(data)
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