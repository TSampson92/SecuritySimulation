import copy

import numpy as N
import numpy.random as rand

#from checkpoint import Checkpoint
from security_simulation.checkpoint import Checkpoint

LOW_WALK_SPEED = 1.25
HIGH_WALK_SPEED = 1.51


class Attendee(object):
    def __init__(self, gender, metal_mean, metal_std_dev, coop_chance, attendee_id, current_location=(0, 0), time_entered=0, has_bag=False):
        """
        Defines the behavior and state of an attendee
        :param gender: gender distribution, float in range [0,1]
        :param metal_mean: mean value of metal for random normal distribution
        :param metal_std_dev: standard deviation of metal for random normal distribution
        :param coop_chance: chance an attendee will be cooperative, between [0,1)
        :param current_location: current location in sim of attendee as (y,x) pair defaults->(0,0)
        :param time_entered: the timestep that the attendee entered the sim defaults->0
        :param has_bag: determines if an attendee has a bag, True/False defaults->False
        """
        # For gender, True == Female, False == Male
        if rand.rand() > gender:
            self.gender = True
        else:
            self.gender = False

        # The percentage of metal that a person has on them, used to determine if this
        # attendee will set off a metal detector at a checkpoint
        self.metal_percent = rand.normal(loc=metal_mean, scale=metal_std_dev)
        # Determine if this attendee is cooperative, if the random value is less than coop chance 
        # then this attendee is cooperative.
        if rand.rand() < coop_chance:
            self.isCooperative = True
        else:
            self.isCooperative = False
        self.current_location = current_location
        self.time_entered = time_entered
        self.bag_check_complete = False
        self.has_bag = has_bag
        self.getting_bag_checked = False
        self.time_step_to_enqueue = 0  # find_checkpoint updates this value
        self.time_step_to_dequeue = 0
        self.total_wait = 0
        self.checkpoint_vector = None
        self.status = 0  # 1= bag_check, 2 = metal detector
        self.checkpoint_target = None
        self.walk_route = [current_location]
        self.attendee_id = attendee_id
        self.walk_speed = rand.uniform(LOW_WALK_SPEED, HIGH_WALK_SPEED)
        self.dist_to_checkpoint = 0.0
        self.at_checkpoint = False
        self.through_security = False
   
    def vec_attendee(gender, metal_mean, metal_std_dev, coop_percent, attendee_id):
        """Method to vectorize the attendee constructor"""
        return _vectorized_attendee(gender, metal_mean, metal_std_dev, coop_percent, attendee_id)

    def _calc_distance(self, checkpoint_loc):
        """ Calculates the distance between this attendee and a checkpoint. 
            This is used by the find_checkpoint method as a factor in determining 
            which checkpoint an attendee will go to.
        """
        return N.sqrt((self.current_location[1] - checkpoint_loc[1])**2 \
                    + (self.current_location[0] - checkpoint_loc[0])**2)
    
    def _set_checkpoint_vector(self, c_loc):
        self.checkpoint_vector = (c_loc[0] - self.current_location[0], c_loc[1] - self.current_location[1])

    def find_checkpoint(self, checkpoints):
        """Finds a checkpoint based on proximity and checkpoint queue size 
        
        The first factor is the proximity of a checkpoint, if a checkpoint is close, line length will be checked
        if length of the line is above a certain tolerance, a further line will be checked. Attenedee will attempt to find 
        the closest checkpoint with the shortest line. If no line is short enough, the agent will use the closest line. 
           
        Variables:
            Checkpoints: List of open checkpoints in current security configuration
        Sets the time_step_to_enque and the checkpoint_target based on the checkpoint the agent decides to go to
        Returns:
            A reference to the target checkpoint that the attendee has chosen
            """
        checkpoint_line_len = N.zeros(len(checkpoints), dtype=float)
        checkpoint_distances = N.zeros(len(checkpoints), dtype=float)

        for i in range(len(checkpoints)):
            checkpoint_line_len[i] = checkpoints[i].get_line_length()
            checkpoint_distances[i] = self._calc_distance(checkpoints[i].location)
        
        min_length = N.min(checkpoint_line_len)
        min_dist = N.min(checkpoint_distances)
        # If the min_length of all lines is > 0, divide all lengths by the min_length
        if (min_length > 0):
            checkpoint_line_len = checkpoint_line_len / min_length
        # Same idea for the distances
        if (min_dist > 0):
            checkpoint_ratios = checkpoint_distances / min_dist
        else:
            checkpoint_ratios = checkpoint_distances
        
        # Add these values together, and choose the smallest value
        checkpoint_rankings = checkpoint_ratios + checkpoint_line_len
        min_index = N.argmin(checkpoint_rankings)
        # found the target checkpoint, set that as the target_checkpoint
        self.checkpoint_target = checkpoints[min_index]
        self._calc_checkpoint_arrival(checkpoint_distances[min_index])
        self._set_checkpoint_vector(self.checkpoint_target.get_location())
        return self.checkpoint_target

    def _calc_checkpoint_arrival(self, distance):
        """ Calculate the time step that an attendee arrives at their target checkpoint 
            distance: the distance in meters from attendee's spawn to the checkpoint
            Generates a random speed in mps from average walking speeds"""
        # From: https://en.wikipedia.org/wiki/Walking, use random float between 4.51() kph (1.25 mps) to 5.43 kph (1.51 mps) to simulate
        # a walking speed
        self.time_step_to_enqueue = int(N.ceil((distance / self.walk_speed)) + self.time_entered)
        self.dist_to_checkpoint = distance
        return self.time_step_to_enqueue

    def calc_total_wait(self, current_time_step):
        """Calculates the total wait time (this is also the total time the attendee spent in the simulation) 
            Current_time_step is the time step at which the attendee exited the simulation (i.e. passed through security.)
            returns:
                The total wait time of the attendee in seconds"""
        self.total_wait = current_time_step - self.time_entered
        return self.total_wait

    def end_queue_time(self, time):
        """
        setter function used to set the end time for an attendee who recently was poped out of queue

        This function is called from checkpoint class. It is called when attendee
        exits the queue and has gone through security. Wait time will stop at this time
        
        :param time: The current time is an integer that be will be passed in as a parameter
        """
        self.time_step_to_dequeue = time

    def _arrived_at_checkpoint(self, current_time):
        """Check if the current attendee should be moved to the checkpoint 

        :param current_time: current timestep to check against

        Returns True if the current time step == this attendee's checkpoint arrival time
        Returns False if not
        """
        if current_time == self.time_step_to_enqueue:
            self.at_checkpoint = True
            return True
        
        return False

    def update(self, time_step):
        """
        Performs a check on an attendee's arrival time at their chosen checkpoint
        If the attendee has arrived, they move into the queue of that checkpoint
        The next step in the route to the checkpoint will also be calculated using inter_step
        :param time_step: The current time step the simulation is at. Compared against the arrival time
                          of the attendee at a checkpoint
        Returns:
            True if the attendee has arrived, the attendee is now in their target checkpoint
            False if they have not, nothing else happens
        """
        if self.at_checkpoint:
            return True

        if self._arrived_at_checkpoint(time_step):
            self.checkpoint_target.add_attendee(self, time_step)
            print("Attendee", self.attendee_id, "at:", self.current_location,\
                "has moved to checkpoint at:", self.checkpoint_target.get_location())
            self.current_location = self.checkpoint_target.get_location()
            self.walk_route[-1] = tuple(self.current_location)
            # print("Attendee Walk Route: ", self.walk_route)
            
            return True
        
        self.inter_step()
        return False
    
    def inter_step(self):
        """
        Interpolates the next point in the attendee's walk route
        Uses the current location, walk speed, and the distance to the checkpoint to
        determine the next point in the attendee's route
        This function will update the attendee's current location to the new point
         """
        #https://math.stackexchange.com/questions/1918743/how-to-interpolate-points-between-2-points
        c_loc = self.checkpoint_target.get_location()
        
        self.dist_to_checkpoint = self._calc_distance(c_loc)
        new_y = self.current_location[0] + (self.walk_speed / self.dist_to_checkpoint \
                                            * (c_loc[0] - self.current_location[0]))
        new_x = self.current_location[1] + (self.walk_speed / self.dist_to_checkpoint \
                                            * (c_loc[1] - self.current_location[1]))
        new_location = [float(new_y), float(new_x)]
        self.current_location = new_location
        self.walk_route.append(new_location)
        
    def get_waiting_in_line(self):
        """
        Return the time the attendee spent waiting in line
        Returns:
            An integer that represents the time that the attendee spent in the
            checkpoint line in seconds
        """
        return self.time_step_to_dequeue - self.time_step_to_enqueue

    def get_time_walking(self):
        """
        Returns how long it took for the attendee to walk to their chosen checkpoint
        Return:
            An integer that represents the time that the attendee spent walking to the 
            checkpoint in seconds.
        """
        return self.time_step_to_enqueue - self.time_entered
    
    def get_time_step_to_enqueue(self):
        """
        Returns the time step that an Attendee will reach their chosen checkpoint
        """
        return self.time_step_to_enqueue

    def to_dict(self):
        """
        Convert object to json like dict representation
        :return: dict containing object data
        """
        base = self.__dict__
        return_dict = {}
        # don't include keys of object references so their value is not overwritten
        bad_keys = ['walk_route', 'current_location', 'checkpoint_target', 'checkpoint_vector']
        for k, v in base.items():
            if k not in bad_keys:
                return_dict[k] = v
        temp_walk_route = []
        # sanitize walk route
        for i in self.walk_route:
            if isinstance(i, N.ndarray):
                temp_walk_route.append(i.tolist())
            else:
                temp_walk_route.append([float(i[0]), float(i[1])])
        return_dict['walk_route'] = temp_walk_route
        return_dict['current_location'] = [float(i) for i in self.current_location] if self.current_location is not None else None
        return_dict['checkpoint_target'] = self.checkpoint_target.id if self.checkpoint_target else None
        return_dict['checkpoint_vector'] = (int(self.checkpoint_vector[0]), int(self.checkpoint_vector[1])) if self.checkpoint_vector else None
        return return_dict

    def to_min_dict(self):
        base = copy.deepcopy(self.to_dict())
        return_dict = {'current_location': base['current_location'],
                       'checkpoint_target': base['checkpoint_target'],
                        'through_security': base['through_security'],
                        'at_checkpoint': base['at_checkpoint']
                       }

        return return_dict

_vectorized_attendee = N.vectorize(Attendee)
