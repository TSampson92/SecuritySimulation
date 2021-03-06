import numpy as N
import matplotlib.pyplot as plt
from security_simulation.filedump import FileDump
from analysis import Analysis

SCALING_FACTOR = 3


class Visualize(object):
    # https://stackoverflow.com/questions/5073386/how-do-you-directly-overlay-a-scatter-plot-on-top-of-a-jpg-image-in-matplotlib
    def __init__(self, sim_file, event_image):
        """
        Simulation class used to visualize the movements of attendees
        :param sim_file: Name of json file that was created when Main.py was run
        :param event_image: Map of tacoma dome
        """
        self.sim_file = sim_file
        self.event_image = event_image

    def plot_sim(self):
        """
        Core function to plot attendee's spawning, and moving to and through a 
        checkpoint
        """
        # Load the simulation output file
        sim_dict = Analysis.load_simulation_file(self.sim_file)
        # Load the image that the visualization will run over
        im = plt.imread(self.event_image)
        implot = plt.imshow(im)

        plt.interactive(True)
        plt.show()
            
        # set the points for the checkpoints
        checkpoints = sim_dict["checkpoints"]

        check_x = N.zeros(len(checkpoints))
        check_y = N.zeros(len(checkpoints))
        for i in range(len(checkpoints)):
            check_loc = checkpoints[i]['location']
            check_x[i] = check_loc[1]
            check_y[i] = check_loc[0]
        check_x = check_x * SCALING_FACTOR
        check_y = check_y * SCALING_FACTOR
        print("Checkpoint count:", len(checkpoints))
        checkpoint_scatter = plt.scatter(check_x, check_y, s=10**2, c='r',label='Security Checkpoints')
         
        # Each key in the sim_dict is a time_step, iterate through and
        # plot the simulation state for attendees
        attendee_scatter = plt.scatter([0],[0])
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        for i in range(len(sim_dict.keys()) - 2):
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
            attendee_scatter = plt.scatter(x_pos, y_pos, c='g',label='Attendees')
            plt.gca().axes.legend(loc='lower right',fontsize = 'x-small')
            plt.draw()
            plt.pause(.1)
            print("Attendee count at timestep", i, ":", attendee_count)        


if __name__ == "__main__":
    #Please provide the name of the json file that was last generated when prompted
    file_name = input("Enter the sim data filename: ")
    if file_name == 'test':
        file_name = 'test_sim_data_file.json'
    vis = Visualize(file_name, "tac_dome.png")
    vis.plot_sim()
