"""Main module to run the Event Security simulation.

Other notes.
"""

import numpy as np

from security_simulation.Model import Model

# For each checkpoint;
# The x coordinate in the space, y coordinate in the space:

CHECKPOINT_LOCATIONS = np.array([
    (10, 10),
    (20, 10)
])

# For each checkpoint;
# Number of bag checkers, metal detectors with operator, checkers for attendees who set off the detector:

SECURITY_PERSONNEL_SETS = np.array([
    [2, 1, 1],
    [3, 1, 1]
])

# The id associated with the checkpoint setup:

CHECKPOINT_CONFIGURATIONS = np.array([0, 1])


ATTENDEE_NUMBER = 10

GENDER_PERCENTAGE = 0.5

METAL_MEAN = 50

METAL_STD_DEV = 17

COOPERATIVE_CHANCE = 90

def __init__():
    model = Model(CHECKPOINT_LOCATIONS, SECURITY_PERSONNEL_SETS, CHECKPOINT_CONFIGURATIONS,
                  ATTENDEE_NUMBER, GENDER_PERCENTAGE, METAL_MEAN, METAL_STD_DEV, COOPERATIVE_CHANCE)
