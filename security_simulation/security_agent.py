
class SecurityAgent:
    ROLES = frozenset(['PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD', 'STANDING'])

    def __init__(self, role='PATDOWN', gender=None):
        """
        :param role: 'PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD', 'STANDING'
        :param gender: F or M
        """
        self.busy = False
        self.busy_until = 0  # time value that agent is free
        self.gender = gender # "F" = female, "M" = male
        self.role = role
        self.assigned_attendee = None
        
    # doing this is essentially a built in getter and setter
    # it uses the getter and setter when using Instance.value syntax
    # https://www.python-course.eu/python3_properties.php
    @property
    def role(self):
        return self.__role
    
    @role.setter
    def role(self, role):
        if role in SecurityAgent.ROLES:
            self.__role = role
        else:
            raise Exception('Invalid Role')

    def test_role(self, role, gender):  # to test that role was set by checkpoint
        """
        test function used to set the role of security agent
        :param role: string that contains the name of the role
        :param gender: string that is either "F" or "M"
        """
        self.role = role           
        self.gender = gender
    
    def set_attendee(self, attendee):
        """
        setter method to assigned an attendee to security personnel to keep them "busy"
        :param attendee: attendee object will be passed to security personnel
        """
        self.assigned_attendee = attendee
    
    def get_attendee(self):
        """
        getter method to retrieve the attendee that was assigned to security
        :return: returns the attendee assigned to a security person
        """
        return self.assigned_attendee