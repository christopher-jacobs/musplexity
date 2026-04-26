from scipy.io.wavfile import read
from window_function import window_function
from visualization import visualize_maximum, persistence_diagram, transformed_visual, cluster_visual
from k_means import sector_count, initializing_centroid, k_means_clustering
from ripser import Rips

import numpy as np
import math

def musiplexity(args):

    # Import wav file and sample rate
    fs, song_data = read(args.wav_file) #fs = sample rate

    t = np.arange(0, 60, 1/44100)
    signal = song_data[0: len(t)]

    # Only capture on speaker worth of data
    split_signal = signal[:, 0]
    temp = max(split_signal)
    split_signal = (1 / temp) * split_signal

    # Create list for max values for each half second (4,410 samples in half of a second)
    max_values = []
    start, end = 0, 4410

    while end <= len(split_signal - 1):
        max_values.append(max(split_signal[start:end]))

        # Shift forward a half second
        start += 4410
        end += 4410
    
    if args.visualize:
        visualize_maximum(args.wav_file, split_signal, max_values)

    # Create a point cloud using the maximum values from the song
    point_cloud = window_function(max_values, args.visualize)
    
    numpy_data = np.array(point_cloud)
    rips = Rips()
    data = rips.fit_transform(numpy_data)

    if args.visualize:
        persistence_diagram(data)

    # Separate the data between H0 and H1
    H0_data, H1_data = data

    # Linearly transform by 45 degrees
    transformed_coords = []
    rad = math.pi/4
    B = np.array([[math.cos(rad), math.sin(rad)], [-(math.sin(rad)), math.cos(rad)]])

    for x in range(len(H1_data)):
        A = np.array([[H1_data[x, 0]], [H1_data[x,1]]])
        C = B@A
        transformed_coords.append(([C[0,0], C[1,0]]))

    if args.visualize:
        transformed_visual(transformed_coords)
    
    matrix = sector_count(transformed_coords)
    centroids = initializing_centroid(matrix, 3)
    centroids = k_means_clustering(np.array(transformed_coords), centroids)

    if args.visualize:
        cluster_visual(np.array(transformed_coords), centroids)
