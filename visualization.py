import numpy as np
import matplotlib.pyplot as plt

from ripser import Rips
from persim import plot_diagrams

def visualize_maximum(song_title, signal, max_values):
    time = np.arange(0, 2646000, 4410)

    x_labels = []

    for x in range(600):
        if(x%100 == 0):
            x_labels.append(x/10)
        else:
            x_labels.append(' ')
    
    # Plot both the signal frequencies and maximum values from the song
    plt.plot(signal)
    plt.plot(time, max_values, '.')
    plt.xticks(time, x_labels, rotation='vertical')
    plt.xlabel("Time (secs)")
    plt.ylabel("Amplitude")
    plt.title(f"60-second Playback of '{song_title.split("\\")[1].split('.')[0]}'")
    plt.show()

def point_cloud_visual(data):
    numpy_data = np.array(data)
    plt.scatter(numpy_data[:,0], numpy_data[:,1])
    plt.title('Point Cloud Diagram')
    plt.show()

def persistence_diagram(data):
    plt.xlim([0,1]), plt.ylim([0,1]), plt.title('Persistence Diagram')
    plot_diagrams(data, show=True)

def transformed_visual(data):
    x_values, y_values = [], []

    for x in range(len(data)):
        x_values.append(data[x][0])
        y_values.append(data[x][1])

    plt.scatter(x_values, y_values)
    plt.xlim([0, 0.5])
    plt.ylim([0, 0.5])
    plt.title('H1 Data Transformed')
    plt.minorticks_on()
    plt.grid(True)
    plt.show()

def cluster_visual(data, centroid):
    plt.scatter(data[:, 0], data[:, 1])
    plt.scatter(centroid[:, 0], centroid[:, 1])

    plt.xlim([0, 0.5])
    plt.ylim([0, 0.5])
    plt.minorticks_on()
    plt.grid(True)
    plt.show()