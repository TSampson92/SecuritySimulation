from security_simulation.attendee import Attendee
from security_simulation.checkpoint import Checkpoint


def test_to_dict():
    """
    test to make sure attendee object is getting converted to dict properly
    :return: None
    """
    a = Attendee(.5, 0.3, .25, .5, 1)
    a.calc_total_wait(550)
    d = a.to_dict()
    assert isinstance(d, dict)
    assert isinstance(a, Attendee)
    assert d['total_wait'] == a.total_wait
    assert d['has_bag'] == a.has_bag


def test_attendee_find_checkpoint():
    att_1 = Attendee(.5, 0.3, .25, .5, 1)
    att_2 = Attendee(.5, 0.3, .25, .5, 2, current_location=(0,5))
    att_3 = Attendee(.5, 0.3, .25, .5, 3, current_location=(5,7))

    check_1 = Checkpoint([])
    check_2 = Checkpoint([], location=(0,6))
    check_3 = Checkpoint([], location=(4,7))

    checkpoints = [check_1, check_2, check_3]
    att_1.find_checkpoint(checkpoints, 0)
    att_2.find_checkpoint(checkpoints, 0)
    att_3.find_checkpoint(checkpoints, 0)

    assert att_1.checkpoint_target is check_1
    assert att_2.checkpoint_target is check_2
    assert att_3.checkpoint_target is check_3


def test_attendee_wait_time():
    att_1 = Attendee(.5, 0.3, .25, .5, 1)
    att_2 = Attendee(.5, 0.3, .25, .5, 2, time_entered=5)
    att_3 = Attendee(.5, 0.3, .25, .5, 3, time_entered=25)

    assert att_1.calc_total_wait(15) == 15
    assert att_2.calc_total_wait(35) == 30
    assert att_3.calc_total_wait(70) == 45


def test_attendee_is_at_checkpoint():
    att_1 = Attendee(.5, 0.3, .25, .5, 1)
    check_1 = Checkpoint([], location=(6,8))
    att_1.find_checkpoint([check_1], 0)
    print("Time it takes attendee to make it to checkpoint: "\
         + str(att_1.get_time_step_to_enqueue()))
    att_1.update(att_1.get_time_step_to_enqueue(), att_1.get_time_step_to_enqueue)
    assert att_1.current_location == check_1.get_location()
    assert check_1.get_line_length() == 1


    