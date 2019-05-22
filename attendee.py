import numpy as N


class Attendee(object):

    def __init__(self, gender, metal_percent, current_location, time_entered, has_bag=False, is_cooperative=True):
        self.gender = gender
        self.metal_percent = metal_percent
        self.current_location = current_location
        self.time_entered = time_entered
        self.has_bag = has_bag
        self.is_cooperative = is_cooperative
    
    def findQueue(self, checkpoints):
    
    def calcTotalWait(self, time_waiting)

