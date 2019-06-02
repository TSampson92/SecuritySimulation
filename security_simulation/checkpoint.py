import random
import uuid
import numpy as np
from security_simulation.security_agent import SecurityAgent
from security_simulation.bag_check import BagCheck
# from security_agent import SecurityAgent
# from bag_check import BagCheck


class Checkpoint(object):
    # constants for check times
    BASE_METAL_TIME = 5
    METAL_VARIANCE = 7

    BASE_WAND_TIME = 10
    WAND_VARIANCE = 10

    BASE_PATDOWN_TIME = 10
    PATDOWN_VARIANCE = 20

    def __init__(self,
                 security_roles,
                 location=(0, 0),
                 attendees_entered_event_ref=None,
                 detection_threshold=60,
                 not_coop_base=5,
                 not_coop_var=10,
                 metal_action='WAND',
                 num_to_bag_check=3):
        """
        Handles a single security checkpoint at an event
        :param security_roles:[bag checkers, person/metal detector, person after detector]
        :param location: location of checkpoint
        :param attendees_entered_event_ref: list to store attendees inside event past security
        :param detection_threshold: level of metal that sets of the metal detector
        :param not_coop_base: base time added for attendees not cooperating
        :param not_coop_var: max variance not cooperating time added to base
        :param metal_action: action taken when attendee sets off detector PATDOWN or WAND
        :param num_to_bag_check: number of attendees back from the front of the line who may bet their bags checked
        """
        self.id = str(uuid.uuid4())
        self.security_agent_list = []
        self.metal_detector_agents = []  # keep an extra ref to metal detector agents for efficiency
        self.security_roles = security_roles
        self.main_queue = []
        self.metal_action = metal_action
        self.detection_threshold = detection_threshold
        self.location = location
        # assigned in assign_roles
        self.bag_check = None
        self.num_metal_detectors = None
        self.assign_roles()

        self.num_to_bag_check = num_to_bag_check
        self.attendees_entered_event = attendees_entered_event_ref
        # replace with empty list when left empty for testing
        if self.attendees_entered_event is None:
            self.attendees_entered_event = []
        self.not_cooperative_time = lambda: random.randint(not_coop_base, not_coop_base + not_coop_var)

    # Security personnel are instantiated and are assigned roles based on input
    # index 0 refers to num of security for bag check
    # index 1 refers to num security in metal detector
    # index 2 refers num of security after detector
    def assign_roles(self):
        """
        Create security agents from security_roles array
        Security personnel are instantiated and are assigned roles based on input
        """
        for index in range(len(self.security_roles)):
            num_agents_of_type = self.security_roles[index]
            role = None
            gender = None
            agent = None
            # index 0 refers to num of security for bag check
            # index 1 refers to num security in metal detector
            # index 2 refers num of security after detector
            for i in range(num_agents_of_type):
                if random.random() < .50:
                    gender = "M"
                else:
                    gender = "F"
                if index == 0:
                    agent = SecurityAgent(role='BAG_CHECK', gender=gender)
                elif index == 1:
                    agent = SecurityAgent(role='METAL_DETECTOR', gender=gender)
                    self.num_metal_detectors = num_agents_of_type
                    self.metal_detector_agents.append(agent)
                elif index == 2:
                    agent = SecurityAgent(role='STANDING', gender=gender)
                self.security_agent_list.append(agent)
                # print("at index:", index, "=", num_agents_of_type, agent.role)
        self.bag_check = BagCheck(self.security_agent_list, checkpoint_id=self.id)
                  
    def add_attendee(self, attendee, current_sim_time):
        """
        adds an attendee to a specific checkpoint queue
        :param attendee: attendee object to add to queue
        :param current_sim_time: current time of the simulation
        :return: length of queue int
        """
        self.main_queue.append(attendee)
        print("Attendee added, queue length now:", len(self.main_queue))
        return len(self.main_queue)

    def __pop_first_attendee(self):
        """
        get and remove first attendee in line
        :return: first attendee in queue
        """
        print("Removed attendee", self.main_queue[0].attendee_id, "from front of queue at checkpoint location:", self.location)
        return self.main_queue.pop(0)

    def metal_detector_update_cycle(self, current_sim_time):
        """
        Perform metal detection on first attendee in line
        admits attendees to events when they have been checked
        :param current_sim_time:
        :return:
        """
        for agent in self.metal_detector_agents:
            # see if agent is ready to admit attendee
            if agent.busy:
                attendee = agent.get_attendee()
                if agent.busy_until <= current_sim_time and attendee is not None:
                    # use busy until instead of current time because it will be an exact entrance time
                    attendee.total_wait = attendee.calc_total_wait(agent.busy_until)
                    attendee.end_queue_time(agent.busy_until)
                    attendee.through_security = True
                    self.attendees_entered_event.append(agent.assigned_attendee)
                    # free agent up
                    agent.busy = False
                    print("Attendee:", attendee.attendee_id, "entered")
                    print("Attendee:", attendee.attendee_id, " used route:", attendee.walk_route)
                    agent.assigned_attendee = None
            if agent.busy or np.size(self.main_queue) == 0:  # agent is still busy:
                pass  # do nothing
            else:
                # grab first in line but to not pop yet
                first_in_line = self.main_queue[0]
                # check bag status
                if first_in_line.has_bag:
                    if not first_in_line.bag_check_complete:
                        # not finished bag check so can't be metal detected
                        break
                # calc time it will take
                detector_time = self.get_total_detector_time(first_in_line.isCooperative, first_in_line.metal_percent, self.metal_action)
                # give attendee to agent
                agent.set_attendee(self.__pop_first_attendee())
                agent.busy = True
                agent.busy_until = current_sim_time + detector_time

    def update(self, current_sim_time):
        """
        update function cycles through the queue, updates status of security
        and pops attendee's that are finished waiting
        :param current_sim_time: current time of the simulation
        """
        self.bag_check.update(self.main_queue, self.num_to_bag_check, current_sim_time)
        self.metal_detector_update_cycle(current_sim_time)

    def get_metal_security(self):  
        """
        get method to return access to security agent list that are in charge of metal_detectors
        :return: list of security agents
        """ 
        return self.metal_detector_agents
    
    def get_security(self):  
        """
        get method to return access to general security agent list 
        :return: list of security agents
        """ 
        return self.security_agent_list
         
    def get_security_num(self):  
        """
        get method to return number of general security agents
        :return: length of general security agents list
        """ 
        return len(self.security_agent_list) 
           
    def get_line_length(self):  
        """
        get method to return length of main_queue which contains attendees
        """ 
        return len(self.main_queue)                                               

    def get_location(self):
        """ 
        get method to return the location at which this checkpoint exists
        """
        return self.location

    def get_total_detector_time(self, cooperative, metal_percent, metal_action):
        """
        calculate time it will take for attendee to go through detector
        :param cooperative: attendee isCooperative
        :param metal_percent: attendee metal_percent
        :param metal_action: checkpoint metal action PATDOWN or WAND
        :return: seconds: int
        """
        time = self.__detector_time()
        if not cooperative:
            time += self.not_cooperative_time()
        if metal_percent >= self.detection_threshold:
            if metal_action == 'WAND':
                time += self.__wand_time()
            elif metal_action == 'PATDOWN':
                time += self.__patdown_time()
        return time

    def to_dict(self):
        base = self.__dict__
        del base['not_cooperative_time']
        del base['attendees_entered_event']

        base['main_queue'] = [attendee.to_dict() for attendee in base['main_queue']]

        base['security_agent_list'] = [agent.to_dict() for agent in base['security_agent_list']]

        base['metal_detector_agents'] = [agent.to_dict() for agent in base['metal_detector_agents']]

        base['bag_check'] = base['bag_check'].to_dict()

        return base

    @staticmethod
    def __detector_time():
        """
        :return:
        """
        return random.randint(Checkpoint.BASE_METAL_TIME, Checkpoint.BASE_METAL_TIME + Checkpoint.METAL_VARIANCE)

    @staticmethod
    def __wand_time():
        """
        :return:
        """
        return random.randint(Checkpoint.BASE_WAND_TIME, Checkpoint.BASE_WAND_TIME + Checkpoint.WAND_VARIANCE)

    @staticmethod
    def __patdown_time():
        """
        :return:
        """
        return random.randint(Checkpoint.BASE_PATDOWN_TIME, Checkpoint.BASE_PATDOWN_TIME + Checkpoint.PATDOWN_VARIANCE)
