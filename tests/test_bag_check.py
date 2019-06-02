from security_simulation.bag_check import BagCheck
from security_simulation.attendee import Attendee
from security_simulation.security_agent import SecurityAgent


def test_bag_check_creation():
    bag_check = get_test_bag_check(2)
    assert len(bag_check.security_personnel) == 2
    agents = bag_check.security_personnel
    assert isinstance(agents[0], SecurityAgent)
    assert agents[0].role == 'BAG_CHECK'
    assert isinstance(agents[1], SecurityAgent)
    assert agents[1].role == 'BAG_CHECK'


def test_check_bags():
    bag_check = get_test_bag_check(2)
    queue = get_test_attendees()
    agents = bag_check.security_personnel
    assert not agents[0].busy and not agents[1].busy
    bag_check.update(queue, 3, 1)
    assert queue[0].getting_bag_checked and queue[1].getting_bag_checked
    assert not queue[0].bag_check_complete and not queue[1].bag_check_complete
    assert agents[0].busy and agents[1].busy
    assert agents[0].assigned_attendee is queue[0]
    search_complete_time_step = agents[0].busy_until
    for i in range(2, search_complete_time_step):
        bag_check.update(queue, 3, i)
    assert agents[0].busy
    assert not queue[0].bag_check_complete
    bag_check.update(queue, 3, search_complete_time_step)
    assert queue[0].bag_check_complete
    assert not queue[0].getting_bag_checked

    for i in range(search_complete_time_step, 300):
        bag_check.update(queue, 3, i)

    for agent in agents:
        assert not agent.busy
        assert agent.assigned_attendee is None
    # check to make sure first three agents have got bags checked
    for attendee in queue[:3]:
        assert attendee.bag_check_complete
        assert not attendee.getting_bag_checked
        assert attendee.has_bag
    # remove agents with check complete
    queue = queue[3:]
    for i in range(search_complete_time_step, 300):
        bag_check.update(queue, 3, i)
    for agent in agents:
        assert not agent.busy
        assert agent.assigned_attendee is None
    # check to make sure next three agents have got bags checked
    for attendee in queue[:3]:
        assert attendee.bag_check_complete
        assert not attendee.getting_bag_checked
        assert attendee.has_bag


def get_test_bag_check(num_agents):
    agents = get_bag_check_personnel(num_agents)
    bag_check = BagCheck(agents)
    return bag_check


def get_test_attendees():
    """
    test attendees for bag_check testing
    :return: list of Attendees with bags
    """
    attendees = [Attendee(.5, 0.3, .25, .5, i) for i in range(10)]
    for attendee in attendees:
        attendee.has_bag = True
    return attendees


def get_bag_check_personnel(num_agents=1):
    return [SecurityAgent('BAG_CHECK', 'F') for i in range(num_agents)]
