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
        #Each key in the sim_dict is a time_step, iterate through and
        #plot the simulation state
        for time_step in sim_dict.keys():
            
        plt.show()
    




if __name__ == "__main__":
    vis = Visualize("sim_out", "tac_dome.png")
    vis.plot_sim()
