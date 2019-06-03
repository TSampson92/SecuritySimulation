import numpy as N
import matplotlib.pyplot as plt
from security_simulation.analysis import Analysis

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
            
        #Each key in the sim_dict is a time_step, iterate through and
        #plot the simulation state
        scatter = plt.scatter([0],[0])
        attendee_count = 0
        for i in range(25):
            print(i)
            
            time_step_dict = sim_dict[str(i)]
            attendee_list = time_step_dict['attendees']
            x_pos = N.zeros(len(attendee_list))
            y_pos = N.zeros(len(attendee_list))
           
            for j in range(len(attendee_list)):
                attendee_count += 1
                attendee = attendee_list[j]
                location = attendee["current_location"]
                x_pos[j] = location[1]
                y_pos[j] = location[0]
            
            x_pos = x_pos * 25
            y_pos = y_pos * 25
            scatter.remove()
            scatter = plt.scatter(x_pos, y_pos,c='g')
            plt.draw()
            plt.pause(.5)
        print("Attendee count:", attendee_count)        

    

if __name__ == "__main__":
    vis = Visualize("SecuritySimulationData_1559520603.583658.json", "tac_dome.png")
    vis.plot_sim()
