"""Simulates the processing of attendees at an event though the security checkpoints, recording the wait times.

Other notes.
"""

import sys

import numpy as np


# from checkpoint import Checkpoint
# from analysis import Analysis
# from spawnpoint import SpawnPoint
from security_simulation.analysis import Analysis
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
                 spawnpoint_locations, spawnpoint_percentages,
                 attendee_number, gender_percentage, metal_mean, metal_std_dev, cooperative_chance,
                 closed_door_time=sys.maxsize, save_simulation=False, minimal_save=True, save_only_final_state=False):
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
        self.parameters = {
            'security_personnel_sets': security_personnel_sets.tolist(),
            'checkpoint_locations': checkpoint_locations.tolist(),
            'spawnpoint_locations': spawnpoint_locations,
            'spawnpoint_percentages': spawnpoint_percentages,
            'attendee_number': attendee_number,
            'gender_percentage': gender_percentage,
            'metal_mean': metal_mean,
            'metal_std_dev': metal_std_dev,
            'cooperative_chance': cooperative_chance,
            'closed_door_time': closed_door_time,
            'spawnpoint_percentages': spawnpoint_percentages
        }
        self.sim_data_analysis = Analysis()
        self.save_sim = save_simulation
        self.save_minimal = minimal_save
        self.save_final_state_only = save_only_final_state
        self.attendee_set = []
        self.spawnpoint_list = []
        self.spawnpoint_percentages = spawnpoint_percentages
        self.attendees_entered_event_set = []
        self.closed_door_time = closed_door_time
        self.max_attendees = attendee_number
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
            self.spawnpoint_list.append(SpawnPoint(closed_door_time, self.spawnpoint_percentages,
                                                   self.attendee_features, max_spawn=3,
                                                   location=spawnpoint_locations[i], 
                                                   total_attendees=attendee_number))

        # Start the simulation.
        self.last_sim_filename = self._sim_loop()

    def _sim_loop(self):
        """
        Core function of program. Attendees will be spawned, checkpoints are updated,
        attendees find their closest checkpoint, and attendees's movements are updated
        through each time step
        :return:
        """
        attendee_id = 0
        # list, num_spawned, attendee_id = spawnpoint.spawn_attendee(self.current_time,attendee_id)
        # While doors have not closed:
        # 1.Spawn new attendees using SpawnPoint 
        # 2.Determine the new attendee's closest checkpoints
        # 3.Update checkpoint's lines to simulate security checks
        # 4.Update every attendee's movements
        self.sim_data_analysis.init_sim_data(self.parameters, self.event_checkpoints)
        while self.current_time < self.closed_door_time:
            print("******** Current time:", self.current_time, "********")
            # spawn new attendees
            newly_added_attendees = 0
            if attendee_id < self.max_attendees:
                for i in range(len(self.spawnpoint_list)):
                    location = self.spawnpoint_list[i]
                    list, num_spawned, attendee_id = location.spawn_attendee(self.current_time,
                                            attendee_id, len(self.attendee_set),self.current_time)
                    newly_added_attendees = newly_added_attendees + num_spawned
                    self.attendee_set = self.attendee_set + list

            # Find the nearest checkpoint for the newly spawned attendee's
            index = len(self.attendee_set) - newly_added_attendees
            while index < len(self.attendee_set):
                attendee = self.attendee_set[index]
                attendee.find_checkpoint(self.event_checkpoints, self.current_time)
                index = index + 1

            # For each checkpoint, simulate its state at this time step.
            for checkpoint_index in np.arange(np.size(self.event_checkpoints)):
                current_checkpoint = self.event_checkpoints[checkpoint_index]
                current_checkpoint.update(self.current_time)

            # update each attendee's position for this time step
            for attendee_index in np.arange(np.size(self.attendee_set)):
                self.attendee_set[attendee_index].update(self.current_time, self.event_checkpoints)

            # dump state for current time step
            if self.save_sim and not self.save_final_state_only:
                self.sim_data_analysis.add_time_step(self.current_time, self.attendee_set,
                                                     self.event_checkpoints, self.attendees_entered_event_set,
                                                     include_attendees=True, include_checkpoints=True, include_entered=False, minimal=self.save_minimal)
            self.current_time += 1

        # save simulation to file
        if self.save_sim:
            if self.save_final_state_only:
                self.sim_data_analysis.add_time_step(self.current_time, self.attendee_set, self.event_checkpoints, self.attendees_entered_event_set,
                                                     include_attendees=True, include_checkpoints=True, minimal=False)
            return self.sim_data_analysis.dump_simulation_to_file()
