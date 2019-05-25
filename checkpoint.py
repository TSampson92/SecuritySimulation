import datetime


class Checkpoint(object):

    def __init__(self, security_personnel, bag_check=None, num_metal_detectors=0):
        self.security_personnel = security_personnel
        self.bag_check = bag_check
        self.num_metal_detectors = num_metal_detectors
        self.check_queue = []

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