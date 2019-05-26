# Both men and women may have bags that will be inspected when going through
# security checks.
import random


class BagCheck:
    def __init__(self, security_personnel: list, attendees_to_check=5,
                 base_search_time=15, search_time_variance=30):
        """
        :param security_personnel: list of security personnel at bag check
        :param attendees_to_check: number of attendees from the front of the
        queue that can have their bag checked in advance of entering
        :param base_search_time: minimum time it takes to search a bag
        :param search_time_variance: max number to add onto base search time
        """
        self.security_personnel = security_personnel
        self.number_to_check = attendees_to_check
        # function to return a random bag search time
        # call like self.bag_check_time()
        self.bag_check_time = lambda: base_search_time + \
                                      random.randint(0, search_time_variance)
        
    def check_bags(self, attendee_queue):
        """
        :param attendee_queue: Queue of attendees waiting for this bag check
        :return:
        """
        for personnel in self.security_personnel:
            pass
            # TODO for each security person at bag check
            # check first three to 5 people in the line for having a bag
            # if they have a bag and a security agent is free have the agent
            # check their bag setting agent to busy for a certain amount of time
