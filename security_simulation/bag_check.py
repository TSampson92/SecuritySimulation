import random
import datetime

class BagCheck:
    def __init__(self, security_personnel: list, attendees_to_check=5,
                 base_search_time=15, search_time_variance=30):
        """
        :param security_personnel: list of security personnel at bag check
        :param attendees_to_check: number of attendees from the front of the
        queue that can have their bag checked in advance of entering
        :param base_search_time: minimum time it takes to search a bag
        :param search_time_variance: max number to add onto base search time
        """
        self.security_personnel = security_personnel
        self.number_to_check = attendees_to_check
        self.metal_detector_queue = []
        self.bag_check_queue = []
        self.bag_check_time = lambda: base_search_time + \
                                      random.randint(0, search_time_variance)
        self.metal_detector_time = base_search_time + random.randint(0, 15)
        
    def cycle_queues(self, main_queue, metal_queue):
        """
        :param attendee_queue: Queue of attendees waiting for this bag check
        """
        attendee_index = 0
        for personnel in self.security_personnel:
            role = personnel.role()
            if personnel.busy() == False and role == "BAG_CHECK":
                if main_queue.len >0:
                    attendee = main_queue[attendee_index]
                    if attendee.status == 0():  #attendee just entered queue
                        if attendee.has_bag() == True:
                            personnel.busy = True
                            personnel.busy_until = datetime.datetime.now().time() + self.bag_check_time
                            attendee_index = attendee_index+1
                            attendee.status = 1   #update their status to 1
                        else: #attendee doesn't have bag move them to metal detector
                            person = main_queue.pop(0)
                            person.status = 1
                            self.metal_detector_queue.append(person)
            elif personnel.busy() == False and role == "METAL_DETECTOR":
                if self.metal_detector_queue.len >0:
                    current_time = datetime.datetime.now().time()
                    self.pop_attendee(current_time)
                    personnel.busy = True
                    personnel.busy_until = current_time + self.metal_detector_time
            #elif personnel.busy() == False and role == "StANDING":    
            elif personnel.busy() == True:
                current_time = datetime.datetime.now().time()
                if personnel.busy_until < current_time: #which means personnel is free
                    personnel.busy = False  
                        
    def pop_attendee(self, current_time):
        """
        update the end time for attendee and then pop off attendee from start of line
        :param current_time: time in seconds from start of simulation
        :return: attendee removed from queue
        """
        if len(self.metal_detector_queue) > 0:
            attendee = self.metal_detector_queue.pop(0)  # pop the first element in queue
            attendee.end_queue_time(current_time)
            attendee.status = 2 
            return attendee                     # return attendee popped off
                    
    def get_bag_check_queue(self):
        """
        function to return the bag_check_queue
        :return: list of attendees at bag_check_queue
        """
        return self.bag_check_queue
        
    def get_metal_detector_queue(self):
        """
        function to return metal_detector_queue
        :return: list of attendees at metal_detector_queue
        """
        return self.metal_detector_queue
        