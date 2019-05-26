"""Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

Other notes.
"""

import numpy as np

from security_simulation.checkpoint import Checkpoint
from security_simulation.attendee import Attendee


class Model:
    event_checkpoints = None
    attendee_set = None

    def __init__(self, checkpoint_positions, security_personnel_sets, checkpoint_configurations,
                 attendee_number, gender_percentage, metal_mean, metal_std_dev, cooperative_chance):
        # Initialize the security check points:

        event_checkpoints = Checkpoint.vecCheckPoint(checkpoint_positions, security_personnel_sets,
                                                     checkpoint_configurations)

        # Create arrays with size of the number of attendees to make, with the arguments to pass in:

        gender_perc_input = np.full(attendee_number, gender_percentage)
        metal_mean_input = np.full(attendee_number, metal_mean)
        metal_std_dev_input = np.full(attendee_number, metal_std_dev)
        cooperative_chance_input = np.full(attendee_number, cooperative_chance)

        # Initialize the attendees:

        attendee_set = Attendee.vecAttendee(gender_perc_input, metal_mean_input,
                                            metal_std_dev_input, cooperative_chance_input)
