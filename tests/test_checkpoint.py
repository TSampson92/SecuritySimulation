from security_simulation.checkpoint import Checkpoint
from security_simulation.attendee import Attendee


def test_checkpoint_creation():
    """
    verify creation of checkpoints is working properly
    :return:
    """
    checkpoint = get_std_test_checkpoint()
    security = checkpoint.get_security()
    # ensure proper number of agents assigned
    assert len(security) == 3

    # ensure proper type assigned
    bag_check_count = 0
    metal_detector_count = 0
    standing_count = 0
    for agent in security:
        if agent.role == 'BAG_CHECK':
            bag_check_count += 1
        elif agent.role == 'STANDING':
            standing_count += 1
        elif agent.role == 'METAL_DETECTOR':
            metal_detector_count += 1
    assert bag_check_count == 1
    assert metal_detector_count == 1
    assert standing_count == 1

    assert checkpoint.bag_check is not None
    assert checkpoint.num_metal_detectors == 1
    assert checkpoint.metal_action == 'WAND'
    assert len(checkpoint.main_queue) == 0
    assert checkpoint.attendees_entered_event == []


def test_add_attendees():
    current_time = 1
    checkpoint = get_std_test_checkpoint()
    attendees = get_test_attendees()
    for i in range(1, len(attendees)+1):
        length = checkpoint.add_attendee(attendees[i-1], current_time)
        assert length == i


def test_pop_attendees():
    current_time = 1
    checkpoint = get_std_test_checkpoint()
    attendees = get_test_attendees()
    for i in range(len(attendees)):
        length = checkpoint.add_attendee(attendees[i], current_time)

    assert len(checkpoint.main_queue) == 10
    # directly access private method for test
    popped = checkpoint._Checkpoint__pop_first_attendee()
    assert len(checkpoint.main_queue) == 9
    assert isinstance(popped, Attendee)


def test_metal_detector():
    current_time = 1
    checkpoint = get_std_test_checkpoint()
    attendees = get_test_attendees()
    for i in range(len(attendees)):
        attendees[i].has_bag = False
        checkpoint.add_attendee(attendees[i], current_time)
    assert len(checkpoint.main_queue) == 10
    current_time += 1
    checkpoint.metal_detector_update_cycle(current_time)
    assert len(checkpoint.main_queue) == 9


def get_std_test_checkpoint():
    bag_checkers = 1
    metal_detector_personnel = 1
    person_after_detector = 1
    roles_list = [bag_checkers, metal_detector_personnel, person_after_detector]
    entered_event = []
    checkpoint = get_test_checkpoint(entered_event, roles_list)
    return checkpoint


def get_test_checkpoint(entered_event_list, security_roles_list):
    """
    get a checkpoint to test with
    :param entered_event_list: list for attendees that have entered the even to go
    :param security_roles_list: [bag checkers, person/metal detector, person after detector]
    :return:
    """
    # Doc on checkpoint creation below
    # Handles a single security checkpoint at an event
    # :param security_roles:[bag checkers, person/metal detector, person after detector]
    # :param location: location of checkpoint
    # :param attendees_entered_event_ref: list to store attendees inside event past security
    # :param detection_threshold: level of metal that sets of the metal detector
    # :param not_coop_base: base time added for attendees not cooperating
    # :param not_coop_var: max variance not cooperating time added to base
    # :param metal_action: action taken when attendee sets off detector PATDOWN or WAND
    # :param num_to_bag_check: number of attendees back from the front of the line who may bet their bags checked
    checkpoint = Checkpoint(security_roles_list,
                            attendees_entered_event_ref=entered_event_list)
    return checkpoint


def get_test_attendees():
    """
    test attendees for checkpoint testing
    :return: list of Attendees
    """
    return [Attendee(.5, 0.3, .25, .5) for i in range(10)]
