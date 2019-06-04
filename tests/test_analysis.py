from security_simulation.attendee import Attendee
from security_simulation.filedump import FileDump
from security_simulation.analysis import Analysis
from security_simulation.checkpoint import Checkpoint
import numpy as N


def test_file_output():
    sim_data = FileDump()
    attendee_list = get_test_attendees()
    checkpoint_list = [get_test_checkpoint(), get_test_checkpoint()]
    sim_data.add_time_step(1, attendee_list, checkpoint_list, [])
    file_name = sim_data.dump_simulation_to_file()
    file = open(file_name, 'r')
    assert file is not None
    file.close()
    loaded_json = Analysis.load_simulation_file(file_name)
    assert isinstance(loaded_json, dict)
    attendees = loaded_json['1']['attendees']
    assert isinstance(attendees, list)
    assert len(attendees) == 5


def get_test_checkpoint():
    bag_checkers = 1
    metal_detector_personnel = 1
    person_after_detector = 1
    roles_list = N.array([bag_checkers, metal_detector_personnel, person_after_detector])
    entered_event = []
    checkpoint = Checkpoint(roles_list)
    return checkpoint


def get_test_attendees():
    attendees = [Attendee(.5, 0.3, .25, .5, i) for i in range(5)]

    return attendees