from security_simulation.security_agent import SecurityAgent


def test_constructor():
    agent = SecurityAgent()
    assert (agent.role == 'PATDOWN')
    assert (agent.gender is None)
    assert (agent.busy is False)
    agent.role = 'BAG_CHECK'
    agent.gender = 'male'
    agent.busy = True
    assert (agent.role == 'BAG_CHECK')
    assert (agent.gender == 'male')
    assert (agent.busy is True)

    try:
        agent.role = 'bad_role'
        assert False
    except:
        assert True
    print('SecurityAgent constructor test passed')