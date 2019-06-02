import numpy as N
import matplotlib.pyplot as plt


class Visualize(object):


    #https://stackoverflow.com/questions/5073386/how-do-you-directly-overlay-a-scatter-plot-on-top-of-a-jpg-image-in-matplotlib
    def __init__(self, sim_file, event_image, image_size):
        self.sim_file = sim_file
        self.event_image = event_image
        self.image_size = image_size

    
    def plot_sim(self):
        im = plt.imread(self.event_image)
        implot = plt.imshow(im)
        plt.scatter([10],[20])

        plt.show()
    
