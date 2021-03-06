import uuid

class SecurityAgent:
    ROLES = frozenset(['PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD', 'STANDING'])
    GENDERS = frozenset(['F', 'M', None])

    def __init__(self, role='PATDOWN', gender=None):
        """
        :param role: 'PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD', 'STANDING'
        :param gender: F or M
        """
        self.busy = False
        self.busy_until = 0  # time value that agent is free
        self.gender = gender  # "F" = female, "M" = male
        self.role = role
        self.assigned_attendee = None
        self.id = str(uuid.uuid4())

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
            raise InvalidSecurityRoleException('Invalid Role')

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        if gender in SecurityAgent.GENDERS:
            self.__gender = gender
        else:
            raise InvalidSecurityGenderException('Invalid Gender')

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

    def to_dict(self):
        """
        Convert object to json like dict representation
        :return: dict containing object data
        """
        base = self.__dict__
        return_dict = {}
        # don't include keys of object references so their value is not overwritten
        bad_keys = ['assigned_attendee']
        for k, v in base.items():
            if k not in bad_keys:
                return_dict[k] = v

        if base['assigned_attendee'] is not None:
            return_dict['assigned_attendee'] = base['assigned_attendee'].to_dict()
        else:
            return_dict['assigned_attendee'] = None
        return return_dict


class InvalidSecurityGenderException(Exception):
    """rasied when gender is set to an invalid value"""
    pass


class InvalidSecurityRoleException(Exception):
    """raised when role is set to an invalid value"""
    pass
