# Both men and women may have bags that will be inspected when going through
# security checks.


class BagCheck:
    def __init__(self, security_personnel: list):
        self.security_personnel = security_personnel
        
    def check_bags(self, attendee_queue):
        for personnel in self.security_personnel:
            pass
            # TODO for each security person at bag check
            # assign them a person with a bag to check if they are not busy
