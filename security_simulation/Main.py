"""Main module to run the Event Security simulation.

Lines involving the creation of the file path to the input_parameters.txt file
are from stackoverflow.com as answer from Andre Caron for the question "How to
reliably open a file in the same directory as a Python script"
"""

import numpy as np
import os
import json

from security_simulation.Model import Model


def run_sim_from_file(file_name):
    INPUT_FILE_PATH = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    INPUT_FILE_PATH = os.path.join(INPUT_FILE_PATH, file_name)

    input_file = open(INPUT_FILE_PATH, 'r')

    input_object = json.loads(input_file.read())

    SECURITY_PERSONNEL_SETS = np.array(input_object["SECURITY_PERSONNEL_SETS"])

    # For each checkpoint;
    # The x coordinate in the space, y coordinate in the space:
    CHECKPOINT_LOCATIONS = np.array(input_object["CHECKPOINT_LOCATIONS"])

    # For each spawnpoint location;
    # The x coordinate in the space, y coordinate in the space:

    SPAWNPOINT_LOCATIONS = input_object["SPAWNPOINT_LOCATIONS"]

    SPAWNPOINT_PERCENTAGES = input_object["SPAWNPOINT_PERCENTAGES"]

    ATTENDEE_NUMBER = input_object["ATTENDEE_NUMBER"]

    GENDER_PERCENTAGE = input_object["GENDER_PERCENTAGE"]

    METAL_MEAN = input_object["METAL_MEAN"]

    METAL_STD_DEV = input_object["METAL_STD_DEV"]

    COOPERATIVE_CHANCE = input_object["COOPERATIVE_CHANCE"]

    SAVE_SIMULATION = input_object["SAVE_SIMULATION"]

    MINIMAL_SAVE = input_object['MINIMAL_SAVE']

    SAVE_ONLY_FINAL_STATE = input_object['SAVE_ONLY_FINAL_STATE']

    CLOSED_DOOR_TIME = input_object['CLOSED_DOOR_TIME']  # seconds

    RUN_UNTIL_DONE = input_object["RUN_UNTIL_DONE"]

    print('--- simulation start ---')
    model = Model(SECURITY_PERSONNEL_SETS, CHECKPOINT_LOCATIONS,
                  SPAWNPOINT_LOCATIONS, SPAWNPOINT_PERCENTAGES,
                  ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV,
                  COOPERATIVE_CHANCE, closed_door_time=CLOSED_DOOR_TIME, save_simulation=SAVE_SIMULATION,
                  minimal_save=MINIMAL_SAVE, save_only_final_state=SAVE_ONLY_FINAL_STATE, run_until_done=RUN_UNTIL_DONE)
    print('--- simulation end ---')
    return model


if __name__ == "__main__":
    run_sim_from_file('input_parameters.txt')


