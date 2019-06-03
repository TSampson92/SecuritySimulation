import numpy as N
import matplotlib.pyplot as plt
from security_simulation.analysis import Analysis

SCALING_FACTOR = 50

class Visualize(object):


    #https://stackoverflow.com/questions/5073386/how-do-you-directly-overlay-a-scatter-plot-on-top-of-a-jpg-image-in-matplotlib
    def __init__(self, sim_file, event_image):
        self.sim_file = sim_file
        self.event_image = event_image

    
    def plot_sim(self):
        #Load the simulation output file
        ana = Analysis()
        sim_dict = ana.load_simulation_file(self.sim_file)
        #Load the image that the visualization will run over
        im = plt.imread(self.event_image)
        implot = plt.imshow(im, aspect='equal')

        plt.interactive(True)
        plt.show()
            
        #set the points for the checkpoints
        print(sim_dict)
        checkpoints = sim_dict["0"]["checkpoints"]

        check_x = N.zeros(len(checkpoints))
        check_y = N.zeros(len(checkpoints))
        for i in range(len(checkpoints)):
            check_loc = checkpoints[i]['location']
            check_x[i] = check_loc[1]
            check_y[i] = check_loc[0]
        check_x = check_x * SCALING_FACTOR
        check_y = check_y * SCALING_FACTOR
        print("Checkpoint count:", len(checkpoints))
        checkpoint_scatter = plt.scatter(check_x, check_y, s=10**2, c='r')
         
        #Each key in the sim_dict is a time_step, iterate through and
        #plot the simulation state for attendees
        attendee_scatter = plt.scatter([0],[0])
        for i in range(25):
            print("******Timestep:", i, "******")
            time_step_dict = sim_dict[str(i)]
            attendee_list = time_step_dict['attendees']
            x_pos = N.zeros(len(attendee_list))
            y_pos = N.zeros(len(attendee_list))
            attendee_count = 0
            for j in range(len(attendee_list)):
                attendee = attendee_list[j]
                location = attendee["current_location"]
                x_pos[j] = N.floor(location[1])
                y_pos[j] = N.floor(location[0])
                attendee_count += 1
            x_pos = x_pos * SCALING_FACTOR
            y_pos = y_pos * SCALING_FACTOR
            attendee_scatter.remove()
            attendee_scatter = plt.scatter(x_pos, y_pos, c='g')
            plt.draw()
            plt.pause(.1)
            print("Attendee count at timestep", i, ":", attendee_count)        

    

if __name__ == "__main__":
    file_name = input("Enter the sim data filename: ")
    vis = Visualize(file_name, "tac_dome.png")
    vis.plot_sim()
