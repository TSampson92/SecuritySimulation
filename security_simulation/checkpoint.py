import random as r
from security_simulation.security_agent import SecurityAgent
from security_simulation.bag_check import BagCheck
# from security_agent import SecurityAgent
# from bag_check import BagCheck


class Checkpoint(object):
    
    def __init__(self, security_roles, bag_check=None, num_metal_detectors=0, location=(0,0)):
        """
        initializes checkpoint object
        :param security_roles: [bag checkers, person/metal detector, person after detector]
        :param bag_check: will be setting this bag_check value later
        :num_metal_detectors: will be setting this num_metal_detectors value later
        """
        self.security_agent_list = []
        self.metal_queue = []
        self.security_roles = security_roles
        self.bag_check = bag_check
        self.num_metal_detectors = num_metal_detectors
        self.main_queue = []
        self.location = location
        self.assign_roles()
    
    #Security personnel are instantiated and are assigned roles based on input
    #index 0 refers to num of security for bag check
    #index 1 refers to num security in metal detector 
    #index 2 refers num of security after detector  
    def assign_roles(self):
        """
        pull apart the list passed in called security_roles
        """
        for index in range(len(self.security_roles)):
            num_of_security = self.security_roles[index]
            i = 0
            while i < num_of_security:
                if r.random() < .50:
                    gender = "M"
                else:
                    gender = "F"
                agent = SecurityAgent()
                if index == 0: 
                    agent.test_role("BAG_CHECK",gender)
                elif index == 1: 
                    agent.test_role("METAL_DETECTOR",gender)
                    self.num_metal_detectors = num_of_security
                elif index == 2 : 
                    agent.test_role("STANDING",gender)
                self.security_agent_list.append(agent)
                i = i+1
                print("at index:", index,"=", num_of_security, agent.role)
        self.bag_check = BagCheck(self.security_agent_list) 
                  
    def add_attendee(self, attendee, current_time):
        """
        adds an attendee to a specific checkpoint queue
        :param attendee: attendee object to add to queue
        :param current_time: time in seconds from start of simulation
        :return: length of queue int
        """
        self.main_queue.append(attendee)
        attendee.start_queue_time(current_time)  # the time attendee has entered queue
        return len(self.main_queue)
    
    def update(self,current_time):
        """
        update function cycles through the queue, updates status of security
        and pops attendee's that are finished waiting
        """
        self.bag_check.cycle_queues(self.main_queue,self.metal_queue)
        self.main_queue = self.bag_check.get_bag_check_queue()
        self.metal_queue = self.bag_check.get_metal_detector_queue()
            
    def get_security(self):  
        """
        get method to return access to security agent list to external classes
        :return: list of security agents
        """ 
        return self.security_agent_list
        
    def get_line_length(self):  
        """
        get method to return length of main_queue which contains attendees
        """ 
        return len(self.main_queue)                                               

    def get_location(self):
        """ 
        get method to return the location at which this checkpoint exists
        """
        return self.location    
    
    def average_wait_time(self):
        """
        calculates the average wait time for a specific checkpoint location
        :return: integer value that represents average wait time
        """
        time_list = self.bag_check.get_wait_time()
        time = sum(time_list) 
        time = time/ len(time_list)
        
def main():
    print("entering main function in checkpoint.py")
    check = Checkpoint([2,1,1])
    # att_1 = Attendee(.5, 0.3, .25, .5)
    # att_2 = Attendee(.5, 0.3, .25, .5, current_location=(0,5))
    # att_3 = Attendee(.5, 0.3, .25, .5, current_location=(5,7))
    # check.add_attendee(att_1)
    # check.add_attendee(att_2)
    # check.add_attendee(att_3)
    print("entering cycle_queues in bag_check")
    check.update()
    