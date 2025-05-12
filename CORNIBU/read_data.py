
import numpy 

def read_data(data):

# Inputs:

# data:
# Type: String
# Description: Path to the .txt file containing the data.

# Output:

# xyz:
# Type: NumPy array
# Description: An array containing the parsed data.

    xyz = list()
    with open(data, 'r') as data:
        for line in data:
            values = [float(v) for v in line.split()[:3]] 
            xyz.append(tuple(values))
    data.close()
    return numpy.array(xyz)
