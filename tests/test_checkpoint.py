from security_simulation.checkpoint import Checkpoint
from security_simulation.attendee import Attendee


def test_checkpoint():
    check = Checkpoint([2, 1, 1])
    att_1 = Attendee(.5, 0.3, .25, .5)
    att_2 = Attendee(.5, 0.3, .25, .5, current_location=(0, 5))
    att_3 = Attendee(.5, 0.3, .25, .5, current_location=(5, 7))
    assert check.add_attendee(att_1, 10) == 1
    assert check.add_attendee(att_2, 20) == 2
    assert check.add_attendee(att_3, 30) == 3

    check.update(40)