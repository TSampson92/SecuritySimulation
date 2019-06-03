"""Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

Other notes.
"""

import sys

import numpy as np

from security_simulation.analysis import Analysis
# from checkpoint import Checkpoint
# from attendee import Attendee
# from spawnpoint import SpawnPoint
from security_simulation.checkpoint import Checkpoint
from security_simulation.spawnpoint import SpawnPoint


class Model:
    """Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

    """

    NO_ONE_BEING_CHECKED = -1

    event_checkpoints = None
    attendee_set = None
    current_time = 0
    closed_door_time = None

    def __init__(self, security_personnel_sets, checkpoint_locations,
                 spawnpoint_locations, spawn_chance, spawn_more_than_one_chance,
                 attendee_number, gender_percentage, metal_mean, metal_std_dev, cooperative_chance,
                 closed_door_time=sys.maxsize, save_simulation=False):
        """Sets up the attendees, checkpoints, and the longest amount of time steps to run for based on the parameters.

        :param checkpoint_positions:
        :param security_personnel_sets:
        :param checkpoint_configurations:
        :param spawnpoint_locations: contains all the potential locations attendee's can spawn
        :param spawn_chance: decimal percentage to determine if an attendee will spawn 
        :param spawn_more_than_one_chance: decimal percentage to determine if more than one attendee will spawn 
        :param attendee_number:
        :param gender_percentage:
        :param metal_mean:
        :param metal_std_dev:
        :param cooperative_chance:
        :param closed_door_time:
        """
        self.sim_data_analysis = Analysis()
        self.save_sim = save_simulation
        self.attendee_set = []
        self.spawnpoint_list = []
        self.attendees_entered_event_set = []
        # Initialize the security check points.
        self.event_checkpoints = np.empty(np.shape(checkpoint_locations)[0], dtype=object)

        for i in np.arange(np.size(self.event_checkpoints)):
            self.event_checkpoints[i] = Checkpoint(security_personnel_sets[i],
                                                   location=checkpoint_locations[i],
                                                   attendees_entered_event_ref=self.attendees_entered_event_set)
            print("checkpoint", i, "==", checkpoint_locations[i])

        self.attendee_features = [gender_percentage, metal_mean, metal_std_dev, cooperative_chance]

        # Initialize the potential spawnpoint locations
        for i in range(len(spawnpoint_locations)):
            self.spawnpoint_list.append(SpawnPoint(spawn_chance, spawn_more_than_one_chance,
                                                   self.attendee_features, max_spawn=3,
                                                   location=spawnpoint_locations[i]))

        self.closed_door_time = closed_door_time
        # self.closed_door_time = 100
        # Start the simulation.
        self.last_sim_filename = self._sim_loop()
        self.max_attendees = attendee_number

    def _sim_loop(self):
        """

        :return:
        """
        attendee_id = 0
        # list, num_spawned, attendee_id = spawnpoint.spawn_attendee(self.current_time,attendee_id)
        # While doors have not closed:
        # 1.Spawn new attendees using SpawnPoint 
        # 2.Determine the new attendee's closest checkpoints
        # 3.Update checkpoint's lines to simulate security checks
        # 4.Update every attendee's movements
        while self.current_time < self.closed_door_time:
            print("******** Current time:", self.current_time, "********")
            # spawn new attendees
            newly_added_attendees = 0
            if (attendee_id < self.max_attendees):
                for i in range(len(self.spawnpoint_list)):
                    location = self.spawnpoint_list[i]
                    list, num_spawned, attendee_id = location.spawn_attendee(self.current_time, attendee_id)
                    newly_added_attendees = newly_added_attendees + num_spawned
                    self.attendee_set = self.attendee_set + list

            # Find the nearest checkpoint for the newly spawned attendee's
            index = len(self.attendee_set) - newly_added_attendees
            while index < len(self.attendee_set):
                attendee = self.attendee_set[index]
                attendee.find_checkpoint(self.event_checkpoints)
                index = index + 1

            # For each checkpoint, simulate its state at this time step.
            for checkpoint_index in np.arange(np.size(self.event_checkpoints)):
                current_checkpoint = self.event_checkpoints[checkpoint_index]
                current_checkpoint.update(self.current_time)

            # update each attendee's position for this time step
            for attendee_index in np.arange(np.size(self.attendee_set)):
                self.attendee_set[attendee_index].update(self.current_time)

            # dump state for current time step
            if self.save_sim:
                self.sim_data_analysis.add_time_step(self.current_time, self.attendee_set,
                                                     self.event_checkpoints, self.attendees_entered_event_set)
            self.current_time += 1

        # save simulation to file
        if self.save_sim:
            return self.sim_data_analysis.dump_simulation_to_file()
