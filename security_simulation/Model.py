"""Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

Other notes.
"""

import sys
import numpy as np

from security_simulation.checkpoint import Checkpoint
from security_simulation.attendee import Attendee


class Model:
    """Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

    """

    NO_ONE_BEING_CHECKED = -1

    event_checkpoints = None
    attendee_set = None
    current_time = 0
    closed_door_time = None

    def __init__(self, security_personnel_sets, checkpoint_locations,
                 attendee_number, gender_percentage, metal_mean, metal_std_dev, cooperative_chance,
                 closed_door_time=sys.maxsize):
        """Sets up the attendees, checkpoints, and the longest amount of time steps to run for based on the parameters.

        :param checkpoint_positions:
        :param security_personnel_sets:
        :param checkpoint_configurations:
        :param attendee_number:
        :param gender_percentage:
        :param metal_mean:
        :param metal_std_dev:
        :param cooperative_chance:
        :param closed_door_time:
        """

        # Initialize the security check points.
        self.event_checkpoints = np.empty(np.shape(checkpoint_locations)[0], dtype=object)

        for i in np.arange(np.size(self.event_checkpoints)):
            self.event_checkpoints[i] = Checkpoint(security_personnel_sets[i], checkpoint_locations[i])

        # Create arrays with size of the number of attendees to make, with the arguments to pass in.

        gender_perc_input = np.full(attendee_number, gender_percentage)
        metal_mean_input = np.full(attendee_number, metal_mean)
        metal_std_dev_input = np.full(attendee_number, metal_std_dev)
        cooperative_chance_input = np.full(attendee_number, cooperative_chance)

        # Initialize the attendees.
        self.attendee_set = Attendee.vec_attendee(gender_perc_input, metal_mean_input, metal_std_dev_input, cooperative_chance_input)
        self.closed_door_time = closed_door_time

        # Start the simulation.

    def sim_loop(self):
        """

        :return:
        """

        # While there are attendees still waiting to get in
        # AND the simulation should not be stopped due to time constraints, run the simulation.
        while np.size(self.attendee_set) > 0 and self.current_time < self.closed_door_time:
            # For each checkpoint, simulate its state at this time step.
            for checkpoint_index in np.arange(np.size(self.event_checkpoints)):
                current_checkpoint = self.event_checkpoints[checkpoint_index]
                current_checkpoint.update(self.current_time)

            for attendee_index in np.arange(np.size(self.attendee_set)):
                self.attendee_set[attendee_index].update(self.current_time)
