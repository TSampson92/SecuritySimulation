
class SecurityAgent:
    ROLES = frozenset(['PATDOWN', 'WAND', 'BAG_CHECK', 'METAL_DETECTOR', 'STANDARD'])
    def __init__(self, role='PATDOWN', gender=None):
        self.busy = False
        self.gender = gender
        self.role = role
    
    @property
    def role(self):
        return self.__role
    
    @role.setter
    def role(self, role):
        if role in SecurityAgent.ROLES:
            self.__role = role
        else:
            raise Exception('Invalid Role')
            
    

def test_constructor():
    agent = SecurityAgent()
    assert(agent.role == 'PATDOWN')
    assert(agent.gender is None)
    assert(agent.busy == False)
    agent.role = 'BAG_CHECK'
    agent.gender = 'male'
    agent.busy = True
    assert(agent.role == 'BAG_CHECK')
    assert(agent.gender == 'male')
    assert(agent.busy == True)

    try:
        agent.role = 'bad_role'
        assert(False)
    except:
        assert(True)
        
    print('SecurityAgent constructor test passed')


            
