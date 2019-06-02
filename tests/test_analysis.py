from security_simulation.attendee import Attendee
from security_simulation.analysis import save_to_json, load_simulation_file


def test_file_output():
    attendee_list = get_test_attendees()
    file_name = save_to_json(attendee_list)
    file = open(file_name, 'r')
    assert file is not None
    file.close()
    loaded_json = load_simulation_file(file_name)
    assert isinstance(loaded_json, dict)
    attendees = loaded_json['attendees']
    assert isinstance(attendees, list)
    assert len(attendees) == 5
    assert attendees[0]['total_wait'] == 1000
    assert attendees[4]['total_wait'] == 1700


def get_test_attendees():
    attendees = [Attendee(.5, 0.3, .25, .5, i) for i in range(5)]
    attendees[0].calc_total_wait(1000)
    attendees[1].calc_total_wait(1500)
    attendees[2].calc_total_wait(500)
    attendees[3].calc_total_wait(2000)
    attendees[4].calc_total_wait(1700)
    return attendees