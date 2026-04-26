from scipy.io.wavfile import read
from ripser import Rips
from persim import plot_diagrams, PersistenceImager
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time

## Import the wav file and sample rate
fs, song_data = read('Humble.wav')  #fs = sample rate

t = np.arange(0, 60, 1/44100)
signal = song_data[0: len(t)]

## Only captures one speaker worth of data
split_signal = signal[:,0]
temp = max(split_signal)
split_signal = (1 / temp) * split_signal

## Creates a list for all max values for each half second in the 60 seconds
maxvalues = []
beginning = 0
end = 4410

while end <= len(split_signal - 1):
    maxvalues.append(max(split_signal[beginning:end]))

    beginning += 4410
    end += 4410

## Creates an array for the y-values of the max values
time = np.arange(0, 2646000, 4410)

x_labels = []

for x in range(600):
    if(x%100 == 0):
        x_labels.append(x/10)
    else:
        x_labels.append(' ')

## Plots both the signal frequencies and maximum values from the song
plt.plot(split_signal)
plt.plot(time, maxvalues, '.')
plt.xticks(time, x_labels, rotation = 'vertical')
plt.xlabel("Time (secs)")
plt.ylabel("Amplitude")
plt.title("60-second Playback of Song's Signal")
plt.show()

## Window Function method for Ripser
def WindowFunction(signal):

  index = 0
  taul = 2
  datapoints = []

  for x in signal:
      window =[signal[index], signal[index + taul]]

      datapoints.append(window)

      index += 1
      if index == (len(signal) - taul):
         return datapoints


## Creates a point cloud using the maximum values from the song
point_cloud = WindowFunction(maxvalues)


## Ripser method for persistence diagrams
def Ripser(data):
    override = np.array(data)
    plt.scatter(override[:,0], override[:,1])
    plt.title('Point Cloud Scatter Plot')
    plt.show()
    rips = Rips()
    diagram = rips.fit_transform(override)
    return diagram


## Creates a persistence diagram using the point cloud data
data = Ripser(point_cloud)
plt.xlim([0,1])
plt.ylim([0,1])
plt.title('Persistence Diagram')
plot_diagrams(data, show = True)

## Separates data between H0 and H1
H0_data = data[0]
H1_data = data[1]

## Use Linear Transformation to Move this 45 degrees
transformed_coordinates = []
rad = math.pi/4
B = np.array([[math.cos(rad), math.sin(rad)], [-(math.sin(rad)), math.cos(rad)]])

for x in range(len(H1_data)):
    A = np.array([[H1_data[x,0]], [H1_data[x,1]]])    
    C = B@A
    transformed_coordinates.append(([C[0,0], C[1,0]]))


## Graphing that shows the new coordinate plane with grid
x_values = []
y_values = []

for x in range(len(transformed_coordinates)):
    x_values.append(transformed_coordinates[x][0])
    y_values.append(transformed_coordinates[x][1])


plt.scatter(x_values, y_values)
plt.xlim([0,0.5])
plt.ylim([0,0.5])
plt.title('H1 Data Transformed')
plt.minorticks_on()
plt.grid(True)
plt.show()

## For loop to count the dot that's located in every sector

y_max = 0.5
y_min = 0.4

x_max = 0.1
x_min = 0.0

matrix = []

for x in range(5):
    vector = []
    for x in range(5):
        count = 0
        for x in range(len(transformed_coordinates)):
            if (transformed_coordinates[x][0] >= x_min and transformed_coordinates[x][0] < x_max and transformed_coordinates[x][1] >= y_min and transformed_coordinates[x][1] < y_max):
              count+= 1
        vector.append(count)
        x_max += 0.1
        x_min += 0.1
    matrix.append(vector)
    y_max -= 0.1
    y_min -= 0.1
    x_max = 0.1
    x_min = 0.0

### Prints all vectors out for visual representation
matrix = np.array(matrix)
print(matrix)

# Randomly pick K (predefined) number of centroids (cluster centres) from
# the datapoints as initial cluster centres (Number of clusters chosen = 3)
data = np.array(transformed_coordinates)

# Checks to see if vector is empty. If so, no centroid will be use
centroids = []
min_range_x = 0.0
max_range_x = 0.1
min_range_y = 0.0
max_range_y = 0.15

for x in range(5):
    total = 0
    
    for y in range(5):
        total += matrix[y][x]

    if total != 0:
        random_x = random.uniform(min_range_x, max_range_x)
        random_y = random.uniform(min_range_y, max_range_y)
        centroids.append((random_x, random_y)) 
        min_range_x += 0.1
        max_range_x += 0.1

    if total == 0:
        centroids.append((0.5,0.5))


centroids = np.array(centroids)
print(centroids)

# For each data point in the dataset, calculate the Euclidean distance
# between itself and each of the K centroids. Assign each data point to
# the closest cluster centre according to the distance measured

data = np.sort(data)
def KMeansAlgorithm(centroids):

    centroidOne = []
    centroidTwo = []
    centroidThree = []
    centroidFour = []
    centroidFive = []

    for x in range(len(data)):
        minimum = 10
        cluster_number = 10
        for y in range(len(centroids)):
            distance = np.sqrt(((data[x][0] - centroids[y][0]) ** 2) + ((data[x][1] - centroids[y][1]) ** 2))
            if(distance < minimum):
                minimum = distance
                cluster_number = y
        if cluster_number == 0:
            centroidOne.append(data[x])
        if cluster_number == 1:
            centroidTwo.append(data[x])
        if cluster_number == 2:
            centroidThree.append(data[x])
        if cluster_number == 3:
            centroidFour.append(data[x])
        if cluster_number == 4:
            centroidFive.append(data[x])


    # Now take the average of all the points in each cluster and reposition
    # the centroids using the newly calculated average

    centroidOne = np.array(centroidOne)
    centroidTwo = np.array(centroidTwo)
    centroidThree = np.array(centroidThree)
    centroidFour = np.array(centroidFour)
    centroidFive = np.array(centroidFive)

    if len(centroidOne) == 0:
        averageOneX = 0.5
        averageOneY = 0.5

    if len(centroidOne) != 0:
        averageOneX = np.mean(centroidOne[:,0])
        averageOneY = np.mean(centroidOne[:,1])

    if len(centroidTwo) == 0:
        averageTwoX = 0.5
        averageTwoY = 0.5

    if len(centroidTwo) != 0:
        averageTwoX = np.mean(centroidTwo[:,0])
        averageTwoY = np.mean(centroidTwo[:,1])

    if len(centroidThree) == 0:
        averageThreeX = 0.5
        averageThreeY = 0.5

    if len(centroidThree) != 0:
        averageThreeX = np.mean(centroidThree[:,0])
        averageThreeY = np.mean(centroidThree[:,1])
    
    if len(centroidFour) == 0:
        averageFourX = 0.5
        averageFourY = 0.5

    if len(centroidFour) != 0:
        averageFourX = np.mean(centroidFour[:,0])
        averageFourY = np.mean(centroidFour[:,1])

    if len(centroidFive) == 0:
        averageFiveX = 0.5
        averageFiveY = 0.5

    if len(centroidFive) != 0:
        averageFiveX = np.mean(centroidFive[:,0])
        averageFiveY = np.mean(centroidFive[:,1])

    newCentroids = [(averageOneX, averageOneY), (averageTwoX, averageTwoY), (averageThreeX, averageThreeY), (averageFourX, averageFourY), (averageFiveX, averageFiveY)]
    newCentroids = np.array(newCentroids)

    ## Measure the distance between the old and new centroids

    final_distances = []

    for x in range(5):
        distance = np.sqrt(((newCentroids[x][0] - centroids[x][0]) ** 2) + ((newCentroids[x][1] - centroids[x][1]) ** 2))
        final_distances.append(distance)

    final_distances = np.array(final_distances)

    # If the distance is 0, then the centroids have been found,
    # else, we go through the process again to find the centroids
    
    if np.sum(final_distances) != 0:
        KMeansAlgorithm(newCentroids)

    if np.sum(final_distances) == 0:
        print(newCentroids)
        plt.scatter(data[:,0], data[:,1])
        plt.scatter(newCentroids[:,0], newCentroids[:,1])
        plt.xlim([0,0.5])
        plt.ylim([0,0.5])
        plt.minorticks_on()
        plt.grid(True)
        plt.show()

KMeansAlgorithm(centroids)