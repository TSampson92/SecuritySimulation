



class Checkpoint(object):

   def __init__(self, security_personnel, num_metal_detectors=0):
       self.security_personnel = security_personnel
       self.num_metal_detectors = num_metal_detectors
       self.check_queue = []
    
   def addAttendee(self, attendee):
       self.check_queue.append(attendee)
       return len(self.check_queue)

