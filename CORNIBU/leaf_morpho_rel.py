import numpy 

def leaf_morpho_rel(nb_segment=100, w0=0.5, lm=0.5):

# Inputs:

# nb_segment:
# Type: Integer
# Default: 100
# Description: Number of segments to divide the leaf shape.

# w0:
# Type: Float
# Default: 0.5
# Description: Parameter for leaf shape calculation.

# lm:
# Type: Float
# Default: 0.5
# Description: Parameter for leaf shape calculation.

# Outputs:

# s:
# Type: NumPy array
# Description: Linear space array ranging from 0 to 1.

# r:
# Type: NumPy array
# Description: Array representing the radial shape of the leaf lamina.

    # Half leaf lamina shape according to oil palm model from Perez 2016
    a0 = w0
    c0 = (w0 - 1) / (lm ** 2)
    b0 = -2 * c0 * lm

    c1 = -1 / (1 - lm) ** 2
    b1 = -2 * c1 * lm
    a1 = -b1 - c1

    s = numpy.linspace(0, 1, nb_segment + 1)
    r1 = numpy.array(a0+b0*s[s <=lm]+c0*s[s <=lm]**2)
    r2 = numpy.array(a1+b1*s[s >lm]+c1*s[s >lm]**2)
    r = numpy.concatenate([r1,r2])

    return s, r
