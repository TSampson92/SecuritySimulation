import datetime


class Checkpoint(object):

    # -------------------------------------------------
    def __init__(self, security_personnel, bag_check=None, num_metal_detectors=0):
        self.security_personnel = security_personnel
        self.bag_check = bag_check
        self.num_metal_detectors = num_metal_detectors
        self.check_queue = []

    # -------------------------------------------------
    # Call this function to add an attendee to a specific checkpoint queue
    # This function returns the length of the queue
    def add_attendee(self, attendee):
        self.check_queue.append(attendee)
        current_time = datetime.datetime.now().time()
        attendee.start_queue_time(current_time)  # the time attendee has entered queue
        # print(current_time)
        return len(self.check_queue)

    # -------------------------------------------------
    # update the end time for attendee and then pop off attendee from start of line
    def pop_attendee(self):
        if len(self.check_queue) > 0:
            attendee = self.check_queue.pop(0)  # pop the first element in queue
            current_time = datetime.datetime.now().time()
            attendee.end_queue_time(current_time)
            return attendee  # return attendee popped off
