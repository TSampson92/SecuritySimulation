
class SecurityAgent:
    ROLES = frozenset(['PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD', 'STANDING'])

    def __init__(self, role='PATDOWN', gender=None):
        self.busy = False
        self.busy_until = 0  # time value that agent is free
        self.gender = gender # "F" = female, "M" = male
        self.role = role
        
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
        self.role = role
        self.busy = True             # once given role, security agent is busy
        self.gender = gender
