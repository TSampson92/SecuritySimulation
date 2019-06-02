from security_simulation.attendee import Attendee
from security_simulation.analysis import Analysis
from security_simulation.checkpoint import Checkpoint


def test_file_output():
    sim_data = Analysis()
    attendee_list = get_test_attendees()
    checkpoint_list = [get_test_checkpoint(), get_test_checkpoint()]
    sim_data.add_time_step(1, attendee_list, checkpoint_list, [])
    file_name = sim_data.dump_simulation_to_file()
    file = open(file_name, 'r')
    assert file is not None
    file.close()
    loaded_json = sim_data.load_simulation_file(file_name)
    assert isinstance(loaded_json, dict)
    attendees = loaded_json['1']['attendees']
    assert isinstance(attendees, list)
    assert len(attendees) == 5
    assert attendees[0]['total_wait'] == 1000
    assert attendees[4]['total_wait'] == 1700


def get_test_checkpoint():
    bag_checkers = 1
    metal_detector_personnel = 1
    person_after_detector = 1
    roles_list = [bag_checkers, metal_detector_personnel, person_after_detector]
    entered_event = []
    checkpoint = Checkpoint(roles_list)
    return checkpoint


def get_test_attendees():
    attendees = [Attendee(.5, 0.3, .25, .5, i) for i in range(5)]
    attendees[0].calc_total_wait(1000)
    attendees[1].calc_total_wait(1500)
    attendees[2].calc_total_wait(500)
    attendees[3].calc_total_wait(2000)
    attendees[4].calc_total_wait(1700)
    return attendees