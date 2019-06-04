"""Main module to run the Event Security simulation.

Lines involving the creation of the file path to the input_parameters.txt file
are from stackoverflow.com as answer from Andre Caron for the question "How to
reliably open a file in the same directory as a Python script"
"""

import numpy as np
import os
import json
from security_simulation.Model import Model

#######################################
# Old keeping for now
#######################################
# # from Model import Model
#
# # For each checkpoint;
# # Number of bag checkers, metal detectors with operator, checkers for attendees who set off the detector:
#
# INPUT_FILE_PATH = os.path.realpath(
#     os.path.join(os.getcwd(), os.path.dirname(__file__)))
#
# INPUT_FILE_PATH = os.path.join(INPUT_FILE_PATH, 'input_parameters.txt')
#
# input_file = open(INPUT_FILE_PATH, 'r')
#
# input_object = json.loads(input_file.read())
#
# SECURITY_PERSONNEL_SETS = np.array(input_object["SECURITY_PERSONNEL_SETS"])
#
# BAG_CHECKERS = np.array(input_object["BAG_CHECKERS"])
#
# #coordinates for checkpoints in tacoma dome using map
# CHECKPOINT_A = (175,108)
# CHECKPOINT_B = (228,126)
# CHECKPOINT_C = (180,120)
# CHECKPOINT_D = (240,252)
# CHECKPOINT_E = (140,180)
# CHECKPOINT_F = (80,180)
#
# # For each checkpoint;
# # The x coordinate in the space, y coordinate in the space:
#
# CHECKPOINT_LOCATIONS = np.array(input_object["CHECKPOINT_LOCATIONS"])
#
# # The id associated with the checkpoint setup:
#
# CHECKPOINT_CONFIGURATIONS = input_object["CHECKPOINT_CONFIGURATIONS"]
#
# #coordinates for parking lots where attendee's will spawn using map
# PARKING_D = (330,124)
# PARKING_E = (285,187)
# PARKING_F = (120,260)
# PARKING_C = (275,46)
# PARKING_H = (20,180)
# PARKING_K = (20,40)
# PARKING_A = (68,34)
#
# # For each spawnpoint location;
# # The x coordinate in the space, y coordinate in the space:
#
# SPAWNPOINT_LOCATIONS = input_object["SPAWNPOINT_LOCATIONS"]
#
# SPAWNPOINT_PERCENTAGES = input_object["SPAWNPOINT_PERCENTAGES"]
#
# ATTENDEE_NUMBER = input_object["ATTENDEE_NUMBER"]
#
# GENDER_PERCENTAGE = input_object["GENDER_PERCENTAGE"]
#
# METAL_MEAN = input_object["METAL_MEAN"]
#
# METAL_STD_DEV = input_object["METAL_STD_DEV"]
#
# COOPERATIVE_CHANCE = input_object["COOPERATIVE_CHANCE"]
#
# SAVE_SIMULATION = input_object["SAVE_SIMULATION"]
#
# MINIMAL_SAVE = False
#
# SAVE_ONLY_FINAL_STATE = False
#
# CLOSED_DOOR_TIME = 300  # seconds
#
#
# def __init__():
#     #print("init start")
#     model = Model(SECURITY_PERSONNEL_SETS, CHECKPOINT_LOCATIONS,
#                   SPAWNPOINT_LOCATIONS, SPAWNPOINT_PERCENTAGES,
#                   ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV,
#                   COOPERATIVE_CHANCE, closed_door_time=CLOSED_DOOR_TIME, save_simulation=SAVE_SIMULATION,
#                   minimal_save=MINIMAL_SAVE, save_only_final_state=SAVE_ONLY_FINAL_STATE)


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

    print('--- simulation start ---')
    model = Model(SECURITY_PERSONNEL_SETS, CHECKPOINT_LOCATIONS,
                  SPAWNPOINT_LOCATIONS, SPAWNPOINT_PERCENTAGES,
                  ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV,
                  COOPERATIVE_CHANCE, closed_door_time=CLOSED_DOOR_TIME, save_simulation=SAVE_SIMULATION,
                  minimal_save=MINIMAL_SAVE, save_only_final_state=SAVE_ONLY_FINAL_STATE)
    print('--- simulation end ---')
    return model


if __name__ == "__main__":
    run_sim_from_file('input_parameters.txt')


