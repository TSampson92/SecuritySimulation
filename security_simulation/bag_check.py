import random
from security_simulation.security_agent import SecurityAgent


class BagCheck:
    def __init__(self, security_personnel: list,
                 base_search_time=5, search_time_variance=25):
        """
        Handles logic for checking attendees bags for an event 
        :param security_personnel: list of security personnel at bag check
        :param base_search_time: minimum time it takes to search a bag
        :param search_time_variance: max number to add onto base search time
        """
        self.security_personnel = []
        # to reduce looping bag check only needs to know about bag checkers
        for person in security_personnel:
            if person.role == 'BAG_CHECK':
                self.security_personnel.append(person)

        self.bag_check_time = lambda: base_search_time + \
                                      random.randint(0, search_time_variance)

    def update(self, queue, num_to_search, current_sim_time):
        """
        Check attendees near front of line and search their bags
        :param queue: checkpoint queue of attendees
        :param num_to_search: number of attendees back from front of line that can get bags searched
        :param current_sim_time: current time of simulation
        :return: None
        """
        attendees_to_search = queue[:num_to_search]
        self.free_up_bag_searchers(current_sim_time)
        # all personal at a bag check are bag checkers
        for agent in self.security_personnel:
            if not agent.busy:  # agent still not busy
                # check first num_to_search in queue for bags
                for attendee in attendees_to_search:
                    if attendee.has_bag and not attendee.bag_check_complete \
                            and not attendee.getting_bag_checked:
                        # setup agent as busy checking bag
                        agent.set_attendee(attendee)
                        agent.busy = True
                        agent.busy_until = current_sim_time + self.bag_check_time
                        # setup agent as busy getting bag checked
                        attendee.getting_bag_checked = True
                        break  # break since found attendee to search
            else:
                pass  # do nothing agent is busy

    def free_up_bag_searchers(self, current_sim_time):
        """
        Check if searchers are done with any bag searches, free up agents, and mark bags as checked
        :param current_sim_time: current time of simulation
        :return: None
        """
        for agent in self.security_personnel:
            if agent.busy:
                attendee = agent.get_attendee()
                if agent.busy_until <= current_sim_time and attendee is not None:
                    # free up agent mark attendee as bags checked
                    attendee.getting_bag_checked = False
                    attendee.bag_check_complete = True
                    agent.busy = False
                    agent.assigned_attendee = None
