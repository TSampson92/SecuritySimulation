# SecuritySimulation
An Agent-Based model of different event security configurations for Tacoma Dome* in Seattle, Washington
*The goal is to abstract to multiple event venues

## -------- INSTALL --------  
from SecuritySimulation directory  
in a terminal run command "pip install ."   

## -------- TESTS --------  
from SecuritySimulation directory  
in a terminal run command "pytest"

## ------- RUNNING --------
* To run the simulation with basic settings:
    1. Run the install
    2. from SecuritySimulation: python security_simulation/Main.py
    3. This will run the default sim - 200 attendees at 500 seconds
    4. Output will be minimal, just the final state of the simulation

Parameters for the simulation can be found in input_parameters.txt, 
the simulation reads all security configurations, spawn locations, and
simulation setup from this file. These values can modified to run different
configurations and simulations.

##Modifiable Parameterss:
* Security Personnel Sets: Should be the same number of lisCheckpointlocations. Defines: [bag checkers, metal detector/person, wand/after check person]

* Checkpoint Locations: Definies the active checkpoints in the simulation. The checkpoints for Tacoma Dome can be defined from this list:
    * CHECKPOINT_A = (175,108)
    * CHECKPOINT_B = (228,126)
    * CHECKPOINT_C = (180,120)
    * CHECKPOINT_D = (240,252)
    * CHECKPOINT_E = (140,180)
    * CHECKPOINT_F = (80,180)
* Spawnpoint Locations: Defines the points that attendees will spawn from. The spawnpoints for Tacoma Dome can be defined from this list:
    * PARKING_D = (330,124)
    * PARKING_E = (285,187)
    * PARKING_F = (120,260)
    * PARKING_C = (275,46)
    * PARKING_H = (20,180)
    * PARKING_K = (20,40)
    * PARKING_A = (68,34)
    **Note: These points are using (y, x) notation.**
* Spawnpoint percentages: The spawn chances for the two halfs of the simulation. The first pair is for the first half of the sim, the second pair is for the second half of the simulation. The format for the pairs of percentages is: [chance an attendee spawns, chance more than one attendee spawns]
* Attendee Number: The number of attendees to be spawned during the course of the simulation
* Gender_Percentage: The chance that an attendee will be male or female
* Metal mean/std dev: Used to generate a uniform random value that represents how much metal an attendee has on them. 
* Cooperative Chance: Chance a spawned attendee is cooperative
* Save_Simulation: This flag will save every timestep of the simulation to a json. 
    **WARNING**: This creates very large files, and slows down the simulation considerably. It is used to build data sets that will be run through the visualization. 
###The Following flags will modify the simulation state:
* Save_only_final state: This flag will only save the state of the simulation at the final time step. It modifes the Save_Simulation flag and is used to save data after very large simulations. 
* Minimal_Save: This modifies the Save_Simulation flag to create a small footprint file for visualization. For large simulations it can still be quite large.
* RUN_UNTIL_DONE: This flag runs the simulation until all attendees have entered the event. It ignores the closed_door parameter.This flag is good for validating the simulation. Set the closed_door time high and run a large amount of attendees and you can see when that number of attendees will enter the event.
        
##Visualizing the attendee walks:
* Visualization is done through visualize_event.py. To run the file:
    1. Place a json dumped from the simulation in the security_simulation folder
    2. Run visualize_event.py
    3. You will be prompted to enter a file name
    4. Enter the name of the json file 
        *  Alt-4. You can enter test, which will use the included test_sim_data_file
    5. The visualization will run


        
## Developers:
* Torren Sampson
    * @TSampson92
* Michael Courter
    * @MichaelCourter64
* Sahjpreet Brar
    * @brars
* Nick Lewis
    * @NickRL21
