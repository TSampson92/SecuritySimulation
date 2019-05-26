


class Checkpoint(object):
    
    def __init__(self, security_personnel, bag_check=None, num_metal_detectors=0):
        """
        initializes checkpoint object
        :param security_personnel: [bag checkers, person/metal detector, person after detector]
        :param bag_check: will be setting this bag_check value later
        :num_metal_detectors: will be setting this num_metal_detectors value later
        """
        self.security_personnel = security_personnel
        self.bag_check = bag_check
        self.num_metal_detectors = num_metal_detectors
        self.check_queue = []
        self.assign_roles()

    def assign_roles(self):
        """
        pull apart the list passed in called security_personnel
        """
        self.bag_check = self.security_personnel[0]
        self.num_metal_detectors = self.security_personnel[1]
        self.bag_check = self.security_personnel[2]
        
    def add_attendee(self, attendee, current_time):
        """
        adds an attendee to a specific checkpoint queue
        :param attendee: attendee object to add to queue
        :param current_time: time in seconds from start of simulation
        :return: length of queue int
        """
        self.check_queue.append(attendee)
        attendee.start_queue_time(current_time)  # the time attendee has entered queue
        # print(current_time)
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

    def update(self, current_time):
        # TODO perform all actions for a timestep
        pass