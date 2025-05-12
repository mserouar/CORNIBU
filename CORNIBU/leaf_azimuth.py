import numpy as np

def leaf_azimuth(size, phyllotactic_angle, phyllotactic_deviation, plant_orientation):

# Inputs:

# size:
# Type: Integer
# Description: Number of leaves.

# phyllotactic_angle:
# Type: Float
# Description: Angle between successive leaves.

# phyllotactic_deviation:
# Type: Float
# Description: Deviation from the main azimuth direction.

# plant_orientation:
# Type: Float
# Description: The orientation of the plant.

# Outputs:

# azim:
# Type: NumPy array
# Description: Array of azimuth angles for each leaf.

    elements = [plant_orientation, np.mod(360-(plant_orientation + 180), 360)]
    probabilities = [0.5, 0.5]
    plant_orientation = np.random.choice(elements, 1, p=probabilities)

    if size == 1:
        return plant_orientation[0]
        
    main = np.arange(0, size) * phyllotactic_angle
    azim = (plant_orientation + main + np.random.uniform(-1, 1, size) * phyllotactic_deviation) % 360

    return azim
