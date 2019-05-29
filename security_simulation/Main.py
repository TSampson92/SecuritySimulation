"""Main module to run the Event Security simulation.

Other notes.
"""

import numpy as np

from security_simulation.Model import Model

# For each checkpoint;
# Number of bag checkers, metal detectors with operator, checkers for attendees who set off the detector:

SECURITY_PERSONNEL_SETS = np.array([
    [2, 1, 1],
    [3, 1, 1]
])

BAG_CHECKERS = np.array([
    True,
    False
])

# For each checkpoint;
# The x coordinate in the space, y coordinate in the space:

CHECKPOINT_LOCATIONS = np.array([
    (10, 10),
    (20, 10)
])



# The id associated with the checkpoint setup:

CHECKPOINT_CONFIGURATIONS = np.array([0, 1])


ATTENDEE_NUMBER = 10

GENDER_PERCENTAGE = 0.5

METAL_MEAN = 0.50

METAL_STD_DEV = 0.17

COOPERATIVE_CHANCE = 0.9


def __init__():
    #print("init start")
    model = Model(SECURITY_PERSONNEL_SETS, CHECKPOINT_LOCATIONS,
                  ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV, COOPERATIVE_CHANCE,
                  closed_door_time=100)

if __name__ == "__main__":
    __init__()
