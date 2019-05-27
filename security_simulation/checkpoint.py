from security_agent import SecurityAgent
from bag_check import BagCheck
import random as r

class Checkpoint(object):
    
    def __init__(self, security_roles, bag_check=None, num_metal_detectors=0):
        """
        initializes checkpoint object
        :param security_roles: [bag checkers, person/metal detector, person after detector]
        :param bag_check: will be setting this bag_check value later
        :num_metal_detectors: will be setting this num_metal_detectors value later
        """
        self.security_agent_list = []
        self.security_roles = security_roles
        self.bag_check = bag_check
        self.num_metal_detectors = num_metal_detectors
        self.check_queue = []
        self.assign_roles()
        

    def assign_roles(self):
        """
        pull apart the list passed in called security_roles
        """
        for index in range(len(self.security_roles)):
            num_of_security = self.security_roles[index]
            i = 0
            while (i < num_of_security):
                if r.random() < .50:
                    gender = "M"
                else:
                    gender = "F"
                agent = SecurityAgent()
                if(index == 0): # index 0 refers to num of security for bag check
                    agent.test_role("BAG_CHECK",gender)
                elif(index == 1): # index 1 refers to num security in metal detector
                    agent.test_role("METAL_DETECTOR",gender)
                    self.num_metal_detectors = num_of_security
                elif(index == 2): # index 2 refers num of security after detector
                    agent.test_role("STANDING",gender)
                self.security_agent_list.append(agent)
                i = i+1
                print("at index:", index,"=", num_of_security)
        self.bag_check = BagCheck(self.security_agent_list) #intialize one bagcheck per queue
               
        
    def add_attendee(self, attendee, current_time):
        """
        adds an attendee to a specific checkpoint queue
        :param attendee: attendee object to add to queue
        :param current_time: time in seconds from start of simulation
        :return: length of queue int
        """
        self.check_queue.append(attendee)
        attendee.start_queue_time(current_time)  # the time attendee has entered queue
        return len(self.check_queue)

    def pop_attendee(self, current_time):
        """
        update the end time for attendee and then pop off attendee from start of line
        :param current_time: time in seconds from start of simulation
        :return: attendee removed from queue
        """
        if len(self.check_queue) > 0:
            attendee = self.check_queue.pop(0)  # pop the first element in queue
            attendee.end_queue_time(current_time)
            return attendee  # return attendee popped off
    
    def update(self,current_time,attendee=None,):
        """
        update function will either add or remove attendee's
        :param current_time: time in seconds from start of simulation
        :param attendee: optional parameter for only when an attendee needs to be added to queue
        """
        if(attendee== None): #check bags when there is no addition to queue
            #self.pop_attendee(current_time)
            self.bag_check.check_bags(self.check_queue)
        else:
            self.add_attendee(attendee,current_time)
            
      
    def get_security(self):  
        """
        get method to return access to security agent list to external classes
        :return: list of security agents
        """ 
        return self.security_agent_list