import random
import datetime

class BagCheck:
    def __init__(self, security_personnel: list,
                 base_search_time=15, search_time_variance=30):
        """
        :param security_personnel: list of security personnel at bag check
        :param base_search_time: minimum time it takes to search a bag
        :param search_time_variance: max number to add onto base search time
        """
        self.security_personnel = security_personnel
        self.metal_detector_queue = []     
        self.main_queue = []
        self.wait_time = []
        self.bag_check_time = lambda: base_search_time + \
                                      random.randint(0, search_time_variance)
        self.metal_detector_time = base_search_time + random.randint(0, 15)
        
    #Function will cycle through all the security, assigning each one an attendee 
    #from the following queues: the main queue and the metal_detector_queue
    #Security will only be assigned an attendee if they are not busy
    #If security is currently busy, check to see if they need to be freed from attendee
    #Once attendee is popped from metal_detector_queue store their wait time in self.wait_time[]   
    def cycle_queues(self, main_queue, metal_queue):
        """
        Core function that cycles through queues updating attendee and security info
        :param main_queue: Queue of attendees waiting for bag check
        :param metal_queue: Queue of attendees waiting for metal detector
        """
        self.metal_detector_queue = metal_queue
        self.main_queue = main_queue
        for personnel in self.security_personnel:
            print("busy: ",personnel.busy, " && role:",personnel.role)
            if personnel.busy == False and personnel.role == "BAG_CHECK":
                if len(self.main_queue) >0:
                    attendee = self.main_queue.pop(0)
                    if attendee.status == 0(): 
                        if attendee.has_bag() == True:
                            personnel.busy = True
                            personnel.busy_until = datetime.datetime.now().time() + self.bag_check_time
                            personnel.set_Attendee(attendee) #give attendee to security
                        else: #attendee doesn't have bag move them to metal detector
                            attendee.status = 1
                            self.metal_detector_queue.append(attendee)
            elif personnel.busy == False and personnel.role == "METAL_DETECTOR":
                if len(self.metal_detector_queue) >0:
                    current_time = datetime.datetime.now().time()
                    attendee = self.metal_detector_queue.pop(0)
                    personnel.busy = True
                    personnel.busy_until = current_time + self.metal_detector_time
                    personnel.set_Attendee(attendee)
            #elif personnel.busy == False and personnel.role == "StANDING":    
            elif personnel.busy == True: 
                current_time = datetime.datetime.now().time()
                if personnel.busy_until < current_time:  #which means personnel is free
                    personnel.busy = False  
                    if personnel.role == "BAG_CHECK":
                        attendee = personnel.get_Attendee() 
                        attendee.status = 1
                        self.metal_detector_queue.append(attendee) #add to next queue
                    elif personnel.role == "METAL_DETECTOR":
                        attendee = personnel.get_Attendee()
                        attendee.status = 2
                        self.end_attendee_time(current_time,attendee) 
                        
    def end_attendee_time(self, current_time, attendee):
        """
        update the end time for attendee and add wait time to list 
        :param current_time: time in seconds from start of simulation
        :param attendee: attendee object passed in
        """
        attendee.end_queue_time(current_time)
        total_time = attendee.calc_total_wait(current_time) 
        self.wait_time.append(total_time)   #keep track of all attendees wait time
                    
    def get_bag_check_queue(self):
        """
        function to return the bag_check_queue
        :return: list of attendees at bag_check_queue
        """
        return self.main_queue
        
    def get_metal_detector_queue(self):
        """
        function to return metal_detector_queue
        :return: list of attendees at metal_detector_queue
        """
        return self.metal_detector_queue
     
    def get_wait_time(self):
        """
        function to return wait time for all attendees
        :return: list of wait times to be calculated 
        """
        return self.wait_time
           
    