import numpy as N
import numpy.random as rand


from security_simulation.checkpoint import Checkpoint

LOW_WALK_SPEED = 1.25
HIGH_WALK_SPEED = 1.51


class Attendee(object):
    # These values are in meters per second

    def __init__(self, gender, metal_mean, metal_std_dev, coop_chance, current_location=(0,0), time_entered=0, has_bag=False):
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
        self.arrives_at_checkpoint = None
        self.total_wait = 0
        self.status = 0 # 1= bag_check, 2 = metal detector
        self.checkpoint_target = None

    
    _vectorized_attendee = N.vectorize(__init__)
   
    def vec_attendee (self, gender, metal_mean, metal_std_dev, coop_percent):
        """Method to vectorize the attendee constructor"""
        return self._vectorized_attendee(gender, metal_mean, metal_std_dev, coop_percent)
    
   
    def calc_distance(self, checkpoint_loc):
        """ Calculates the distance between this attendee and a checkpoint. 
            This is used by the find_checkpoint method as a factor in determining 
            which checkpoint an attendee will go to.
        """
        return N.sqrt((self.current_location[1] - checkpoint_loc[1])**2 \
                    + (self.current_location[0] - checkpoint_loc[0])**2)

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
            checkpoint_distances[i] = self.calc_distance(checkpoints[i].location)
        
        min_length = N.min(checkpoint_line_len)
        min_dist = N.min(checkpoint_distances)
        # If the min_length of all lines is > 0, divide all lengths by the min_length
        if (min_length > 0):
            checkpoint_line_len = checkpoint_line_len / min_length
        # Same idea for the distances
        if (min_dist > 0):
            checkpoint_ratios = checkpoint_distances / min_dist
        
        # Add these values together, and choose the smallest value
        checkpoint_rankings = checkpoint_ratios + checkpoint_line_len
        min_index = N.argmin(checkpoint_rankings)
        # found the target checkpoint, set that as the target_checkpoint
        self.checkpoint_target = checkpoints[min_index]
        self.calc_checkpoint_arrival(checkpoint_distances[min_index])
        return self.checkpoint_target

    def calc_checkpoint_arrival(self, distance):
        """ Calculate the time step that an attendee arrives at their target checkpoint 
            distance: the distance in meters from attendee's spawn to the checkpoint
            Generates a random speed in mps from average walking speeds"""
        # From: https://en.wikipedia.org/wiki/Walking, use random float between 4.51() kph (1.25 mps) to 5.43 kph (1.51 mps) to simulate
        # a walking speed
        attendee_speed = rand.uniform(LOW_WALK_SPEED, HIGH_WALK_SPEED)
        self.time_step_to_enqueue = N.ceil((distance / attendee_speed)) + self.time_entered
        return self.time_step_to_enqueue

    def calc_total_wait(self, current_time_step):
        """Calculates the total wait time (this is also the total time the attendee spent in the simulation) 
            Current_time_step is the time step at which the attendee exited the simulation (i.e. passed through security.)
            returns:
                The total wait time of the attendee in seconds"""
        self.total_wait = current_time_step - self.time_entered
        return self.total_wait

    def start_queue_time(self, time):
        """setter function used to set the start time for an attendee who recently was added to a queue 
           
        This function is called from checkpoint class. Used to store the start time for an attendee's queue experience   
        
        Variables
        time: The current time is an integer that be will be passed in as a parameter
  
            """
        self.time_step_to_enqueue = time

    def end_queue_time(self, time):
        """setter function used to set the end time for an attendee who recently was poped out of queue 
           
       This function is called from checkpoint class. It is called when attendee 
       exits the queue and has gone through security. Wait time will stop at this time 
        
        Variables
        time: The current time is an integer that be will be passed in as a parameter
  
            """
        self.time_step_to_dequeue = time

    def arrived_at_checkpoint(self, current_time):
        """Check if the current attendee should be moved to the checkpoint 
            Returns True if the current time step == this attendee's checkpoint arrival time
            Returns False if not """
        if (current_time == self.arrives_at_checkpoint):
            return True
        
        return False

    def update(self, time_step):
        """ Performs a check on an attendee's arrival time at their chosen checkpoint
                If the attendee has arrived, they move into the queue of that checkpoint
            Parameters: 
                time_step: The current time step the simulation is at. Compared against the arrival time
                    of the attendee at a checkpoint
            Returns:
                True if the attendee has arrived, the attendee is now in their target checkpoint
                False if they have not, nothing else happens"""
        if self.arrived_at_checkpoint(time_step):
            self.start_queue_time(time_step)
            self.checkpoint_target.add_attendee(self, time_step)
            return True
        
        return False
    
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
        return self.arrives_at_checkpoint - self.time_entered

    def to_dict(self):
        """
        Convert object to json like dict representation
        :return: dict containing object data
        """
        data = {
            'gender': self.gender,
            'metal_percent': self.metal_percent,
            'isCooperative': self.isCooperative,
            'current_location': self.current_location,
            'bag_check_complete': self.bag_check_complete,
            'has_bag': self.has_bag,
            'time_step_to_enqueue': self.time_step_to_enqueue,
            'time_step_to_dequeue': self.time_step_to_dequeue,
            'arrives_at_checkpoint': self.arrives_at_checkpoint,
            'total_wait': self.total_wait,
            'status': self.status,
            'check_point_target': self.checkpoint_target
        }
        return data
