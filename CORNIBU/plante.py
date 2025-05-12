from leafsize import leafsize
from leaf_shape_rank import *
import numpy as np

def plante(N_max, S_max, H_max, incli_top, incli_base, l, delta):

# Inputs:

# N_max:
# Type: Integer
# Description: Number of leaves.

# S_max:
# Type: Float
# Description: Total leaf area of the plant in square meters (m²).
                                                            
# H_max:
# Type: Float
# Description: Height of the plant in meters (m).

# Outputs:

# ABC_stem:
# Type: List of lists (nested lists)
# Description: Represents the geometry of the stem in 3D space.

# ABC_leaf:
# Type: NumPy array
# Description: Represents the geometry of the leaves in 3D space.

# s_leaff:
# Type: NumPy array
# Description: Surface area of the leaves (for theoretical LAI computation).

# longueur:
# Type: NumPy array
# Description: Represents the length of leaves.

    leaf_shape, longueur = leafsize(S_max, N_max)           # Calculate the shape (ratio length-width) of the leaf and its length

    a = 0.59526                                             # Model parameters from Koetz 2001
    d = 1.4158

    N = np.arange(1, N_max+1)
    S = (1+np.sin((np.pi/a)*((N/N_max)**d)-(np.pi/2)))/2    # Leaf area for each leaf order 
    Summ = S.sum()
    SS = S*S_max/Summ                                       # Normalizing the maximum leaf area produced

    b_leaff = np.sqrt(2*SS*leaf_shape)                      # Base of the leaves (max width as for now leaves will be isoceles triangles)
    h_leaff = np.sqrt(2*SS/leaf_shape)                      # Length of the leaves (as for now leaves will flat in a same direction, parallel to ground)
    s_leaff = b_leaff*h_leaff/2                             # Initialize Surface for isoceles triangles | Useful for theorical LAI computation

    #print('suface model by leaf', s_leaff)

    Euclidian_distance_length = []
    for Leaf_OI in N :
        x_max, y_max = leaf_shape_rank(rank = Leaf_OI-1, incli_top = incli_top, incli_base = incli_base, l = l, delta = delta, nb_segment = int(longueur[Leaf_OI-1]*100))       # Curvature and inclination function
        Euclidian_distance_length.append(np.abs((x_max[np.argmax(x_max)]-x_max[0])/100))

    ABC_leaf = np.zeros((N_max, 9))                         # Leaves building
    ABC_leaf[:,1] = b_leaff/40
    ABC_leaf[:,3] = Euclidian_distance_length
    ABC_leaf[:,7] = b_leaff/40

    r_stem_N_max = 20*H_max/2.5                             # Stem building
    r_stemm = []

    for i in N :
        r_stemm.append(0.02 + (r_stem_N_max - 0.02)/ (N_max-1)* (i-1))
    ABC_stem = []
    for i in N :
        ABC_stem.append( [[r_stemm[i-1] ,0 ,0, 0 ,r_stemm[i-1] ,0, 0, 0, H_max] , [0, r_stemm[i-1], 0 ,-r_stemm[i-1], 0 ,0, 0 ,0, H_max ], [-r_stemm[i-1] ,0, 0, 0 ,-r_stemm[i-1], 0, 0, 0, H_max], [0, -r_stemm[i-1], 0 ,r_stemm[i-1], 0 ,0, 0, 0 , H_max]] )         

    return ABC_stem, ABC_leaf, s_leaff, longueur


