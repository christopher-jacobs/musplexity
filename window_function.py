from visualization import point_cloud_visual

def window_function(signal, visualize):

    index = 0
    taul = 2
    datapoints = []

    for x in signal:
        window = [signal[index], signal[index + taul]]

        datapoints.append(window)

        index += 1

        if index == (len(signal) - taul):
            if(visualize):
                point_cloud_visual(datapoints)
                return datapoints
            else:
                return datapoints