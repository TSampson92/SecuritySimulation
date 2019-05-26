
class SecurityAgent:
    ROLES = frozenset(['PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD'])

    def __init__(self, role='PATDOWN', gender=None):
        self.busy = False
        self.busy_until = 0  # time value that agent is free
        self.gender = gender
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
