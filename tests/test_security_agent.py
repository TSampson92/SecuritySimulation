from security_simulation.security_agent import SecurityAgent, InvalidSecurityRoleException,\
    InvalidSecurityGenderException
from security_simulation.attendee import Attendee


def test_security_agent_creation():
    agent = SecurityAgent()
    assert (agent.role == 'PATDOWN')
    assert (agent.gender is None)
    assert (agent.busy is False)
    agent.role = 'BAG_CHECK'
    agent.gender = 'M'
    agent.busy = True
    assert (agent.role == 'BAG_CHECK')
    assert (agent.gender == 'M')
    assert (agent.busy is True)

    try:
        agent.role = 'bad_role'
        assert False
    except InvalidSecurityRoleException:
        assert True

    try:
        agent.gender = 'invalid_gender'
        assert False
    except InvalidSecurityGenderException:
        assert True

    print('SecurityAgent constructor test passed')


def test_attendee_assignment():
    attendee = Attendee(.5, 0.3, .25, .5, 10)
    agent = SecurityAgent('BAG_CHECK', gender='F')
    assert agent.assigned_attendee is None
    agent.set_attendee(attendee)
    assert agent.get_attendee() is attendee
