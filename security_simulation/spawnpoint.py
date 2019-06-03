import numpy as N
import numpy.random as rand

#from attendee import Attendee
from security_simulation.attendee import Attendee


class SpawnPoint(object):
    
    def __init__(self, spawn_chance, spawn_more_than_one_chance, attendee_init_params, max_spawn=3, location=(0, 0), total_attendees=10):
        """
        Defines an attendee entrance (spawn) point into the simulation
        :param spawn_chance: defines the chance that an attendee will spawn at any give time step. values in range [0,1)
        :param spawn_more_than_one_chance: chance that more than one attendee will spawn at a single spawn point, in 
               any given spawn point. values in range [0,1)
        :param attendee_init_params: a list of parameters that will define attendees, the order of parameters being the exact order
               of parameters in the attendee class __init__ method
        :param max_spawn: The maximum number of attendees that could be spawned at any given time step defaults->3
        :param location: They (y,x) location of the spawn point defaults->(0,0)
        """
        self.spawn_chance = spawn_chance
        self.spawn_more_than_one_chance = spawn_more_than_one_chance
        self.attendee_init_params = attendee_init_params
        self.attendee_gender_per = attendee_init_params[0]
        self.attendee_metal_mean = attendee_init_params[1]
        self.attendee_metal_std_dev = attendee_init_params[2]
        self.attendee_coop_chance = attendee_init_params[3]
        self.max_spawn = max_spawn
        self.total_attendees = total_attendees
        self.location = location

    def spawn_attendee(self, current_time_step, current_id_num, current_num_attendees):
        """
        Called at each timestep at a Spawnpoint to spawn between 0 and self.max_spawn attendees. 
        If an attendee is spawned, there is another chance that more than one will be spawned.
        :param current_time_step: The current timestep of the simulation. This will be the simulation 
                                  time for all attendees spawned in this call of the method
        :param current_id_num:passed in most current attendee id being used                          
        """
        num_to_spawn = 0
        spawned_attendies = []
        if rand.random() < self.spawn_chance:
            if rand.random() < self.spawn_more_than_one_chance:
                num_to_spawn = rand.randint(2, self.max_spawn)
            else:
                num_to_spawn = 1
            print("num spawned =", num_to_spawn)
            if num_to_spawn + current_num_attendees > self.total_attendees:
                num_to_spawn = self.total_attendees - current_num_attendees
            for i in range(num_to_spawn):
                current_id_num = current_id_num + 1
                enter_ye = Attendee(self.attendee_gender_per,
                                    self.attendee_metal_mean,
                                    self.attendee_metal_std_dev,
                                    self.attendee_coop_chance,
                                    attendee_id=current_id_num,
                                    current_location=self.location,
                                    time_entered=current_time_step,
                                    has_bag=rand.randint(0, 1),
                                    )
                print("attendee_id =", current_id_num)                    
                spawned_attendies.append(enter_ye)
        return spawned_attendies, num_to_spawn, current_id_num
    
    def get_spawn_chance(self):
        """
        Getter method to return the chance of an attendee spawning  
        :return:chance that an is attendee spawning                  
        """
        return self.spawn_chance
        
    def set_spawn_chance(self, chance):
        """
        Setter method to set the chance of an attendee spawning                       
        """
        self.spawn_chance = chance
        
    def get_spawn_many_chance(self):
        """
        Getter method to return the chance of multiple attendees spawning  
        return:chance that multiple attendees are spawning                        
        """
        return self.spawn_more_than_one_chance
        
    def set_spawn_many_chance(self, chance):
        """
        Setter method to set the chance of an attendee spawning more than once                        
        """
        self.spawn_more_than_one_chance = chance
        
    def set_max_spawn(self,spawn_num):
        """
        Setter method to set the chance of an attendee spawning more than once                        
        """ 
        self.max_spawn = spawn_num