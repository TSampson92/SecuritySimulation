"""Main module to run the Event Security simulation.

Other notes.
"""

import numpy as np

from security_simulation.Model import Model
# from Model import Model

# For each checkpoint;
# Number of bag checkers, metal detectors with operator, checkers for attendees who set off the detector:

SECURITY_PERSONNEL_SETS = np.array([
    [2, 1, 1],
    [3, 1, 1],
    [3,1,1]
])

BAG_CHECKERS = np.array([
    True,
    False
])

#coordinates for checkpoints in tacoma dome using map
CHECKPOINT_A = (175,108)
CHECKPOINT_B = (228,126)
CHECKPOINT_C = (180,120)
CHECKPOINT_D = (240,252)
CHECKPOINT_E = (140,180)
CHECKPOINT_F = (80,180)

# For each checkpoint;
# The x coordinate in the space, y coordinate in the space:
# CHECKPOINT_LOCATIONS = np.array([
#     CHECKPOINT_A,
#     CHECKPOINT_F
# ])
CHECKPOINT_LOCATIONS = np.array([
    CHECKPOINT_A,
    CHECKPOINT_B,
    CHECKPOINT_D
])

# The id associated with the checkpoint setup:

CHECKPOINT_CONFIGURATIONS = np.array([0, 1])

#coordinates for parking lots where attendee's will spawn using map
PARKING_D = (330,124)
PARKING_E = (285,187)
PARKING_F = (120,260)
PARKING_C = (275,46)
PARKING_H = (20,180)
PARKING_K = (20,40)
PARKING_A = (68,34)

# For each spawnpoint location;
# The x coordinate in the space, y coordinate in the space:
# SPAWNPOINT_LOCATIONS = [
#     PARKING_H,
#     PARKING_K,
# ]
SPAWNPOINT_LOCATIONS = [
    PARKING_D,
    PARKING_E,
    PARKING_A,
    PARKING_C
]


SPAWNPOINT_PERCENTAGES = [
    (.70, .20),
    (.20, .10),
]

ATTENDEE_NUMBER = 200

GENDER_PERCENTAGE = 0.5

METAL_MEAN = 0.50

METAL_STD_DEV = 0.17

COOPERATIVE_CHANCE = 0.9

SAVE_SIMULATION = True



def __init__():
    #print("init start")
    model = Model(SECURITY_PERSONNEL_SETS, CHECKPOINT_LOCATIONS,
                  SPAWNPOINT_LOCATIONS, SPAWNPOINT_PERCENTAGES,
                  ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV, 
                  COOPERATIVE_CHANCE, closed_door_time=500, save_simulation=SAVE_SIMULATION)


if __name__ == "__main__":
    __init__()