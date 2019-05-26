import numpy as N


class Attendee(object):
    def __init__(self, gender, metal_percent, current_location, time_entered, has_bag=False, is_cooperative=True):
        self.gender = gender
        self.metal_percent = metal_percent
        self.current_location = current_location
        self.time_entered = time_entered
        self.back_check_complete = False
        self.has_bag = has_bag
        self.is_cooperative = is_cooperative
        self.time_step_to_enqueue = 0  # checkpoint class updates this value
        self.time_step_to_dequeue = 0
        self.checkpoint_target = None
    
    def find_checkpoint(self, checkpoints):
        """Finds a checkpoint based on proximity and checkpoint queue size 
        
        The first factor is the proximity of a checkpoint, if a checkpoint is close, line length will be checked
        if length of the line is above a certain tolerance, a further line will be checked. Attenedee will attempt to find 
        the closest checkpoint with the shortest line. If no line is short enough, the agent will use the closest line. 
           
        Variables
        Checkpoints: List of open checkpoints in current security configuration

        Sets the time_step_to_enque and the checkpoint_target based on the checkpoint the agent decides to go to   
            """
        pass 
    
    def calc_total_wait(self, time_waiting):
        pass


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
