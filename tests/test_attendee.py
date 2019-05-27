from security_simulation.attendee import Attendee


def test_to_dict():
    """
    test to make sure attendee object is getting converted to dict properly
    :return: None
    """
    a = Attendee(.5, 0.3, .25, .5)
    a.calc_total_wait(550)
    d = a.to_dict()
    assert isinstance(d, dict)
    assert isinstance(a, Attendee)
    assert d['total_wait'] == a.total_wait
    assert d['has_bag'] == a.has_bag
