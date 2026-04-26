from rock_cluster import get_rock_songs
from country_cluster import get_country_songs

import numpy as np

def sector_count(data):

    # Turn data into numpy array and get dimension length
    data = np.array(data)
    dim, _ = data.shape

    # Create bins
    xedges = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    yedges = xedges

    # Slice data and reshape from (N, 1) to (N)
    x = data[:, :1].reshape(dim)
    y = data[:, 1:2].reshape(dim)

    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    # Return rotated matrix
    return np.rot90(H)


def initializing_centroid(data, N):

    centroids = []

    min_range_x = 0.0
    max_range_x = 0.1

    total = np.sum(data, axis=0)

    for x in range(5):

        if total[x] != 0:
            random_x = np.random.uniform(min_range_x, max_range_x)
            random_y = np.random.uniform(0.0, 0.15)
            centroids.append((random_x, random_y)) 
            min_range_x += 0.1
            max_range_x += 0.1

        if total[x] == 0:
            centroids.append((0.5,0.5))
    
    return np.array(centroids)


def k_means_clustering(data, centroids):

    new_centroid = []
    country_songs = get_country_songs()
    
    #centroid = country_songs[np.random.randint(0,63)]

    for x in range(64):
        temp = 0
        for y in range(44):
            temp += country_songs[y][x]
        new_centroid.append(temp/64)

    final_distances = []

    for x in range(len(centroids)):
        distance = np.linalg.norm(new_centroid[x] - centroids[x])
        final_distances.append(distance)

    if np.sum(final_distances) == 0:
        return new_centroid
    else:
        k_means_clustering(data, new_centroid)