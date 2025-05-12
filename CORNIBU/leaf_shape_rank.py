from leaf_shape import leaf_shape
import numpy as np

def leaf_shape_rank(rank, nb_segment, incli_top, incli_base, l, delta):

# Inputs:

# rank:
# Type: Integer
# Description: Rank of the leaf.

# nb_segment:
# Type: Integer
# Description: Number of segments to divide the leaf shape.

# incli_top:
# Type: Float
# Description: Inclination from the highest leaf.

# incli_base:
# Type: Float
# Description: Inclination from the lowest leaf.

# l:
# Type: Float
# Description: Length leaf ratio where curvature occurs.

# delta:
# Type: Float
# Description: Curvature governed by the intersection between leaf insertion angle and leaf tip angle.

# Output:

# Returns the result of calling the function leaf_shape() with specific parameters.

    phytomer=16
    dinc = float(incli_top - incli_base) / (phytomer - 1)
    incli = incli_base + (rank -1) * dinc
    
    tip_angle = incli_base + delta
    a = np.log(240/tip_angle - 1)
    b = 4*0.02
    infl = a / b + incli_base

    return leaf_shape(nb_segment = nb_segment, insertion_angle = incli, l=l, infl=infl)

