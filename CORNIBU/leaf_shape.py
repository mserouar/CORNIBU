import numpy as np

def leaf_shape(nb_segment, insertion_angle, l, infl):

# Inputs:

# nb_segment:
# Type: Integer
# Description: Number of segments to divide the leaf shape.

# insertion_angle:
# Type: Float
# Description: The angle at which the leaf is attached to the stem.

# infl:
# Type: Float
# Description: Inflection point for the sigmoid function.

# l:
# Type: Float
# Description: Length of the leaf.

# Outputs:

# x:
# Type: NumPy array
# Description: x coordinates of the leaf profile.

# y:
# Type: NumPy array
# Description: y coordinates of the leaf profile.

    def _sigmo(x,max,slope,infl):
        # Sigmoid function with a given maximum value, slope, and inflection point
        return(max / (1+np.exp(4*slope*(infl-x))))

    def _curvature(s, coef_curv):
        # Calculate the curvature of the leaf shape based on a given segment length and a coefficient of curvature
        return ((1 + coef_curv) * (s**2)) / (1 + coef_curv * (s**2))

    s = np.linspace(0,1,nb_segment+1)
    frac_l = 2. / 3
    coefCurv_1 = -0.2
    coefCurv_2 = 5

    tip_angle = np.maximum(insertion_angle, _sigmo(x=insertion_angle, max=240, slope=0.02, infl=infl))
    l_angle = insertion_angle + frac_l*(tip_angle - insertion_angle)
    angle_simu_1 = _curvature(s, coef_curv=coefCurv_1) * np.radians(l_angle-insertion_angle) + np.radians(insertion_angle)      # Before curvature break
    angle_simu_2 = _curvature(s[1:], coef_curv=coefCurv_2) * np.radians(tip_angle - l_angle) + np.radians(l_angle)              # After curvature break
    angle_simu=np.array(angle_simu_1.tolist() + angle_simu_2.tolist())
    coef_l=[l]*len(s)+[1-l]*len(s[1:])
    dx = np.array([0] + (coef_l * np.sin(angle_simu)).tolist())[:-1]                                                            # Changes (dx) in the x-coordinates for each segment of the leaf shape
    dy = np.array([0] + (coef_l * np.cos(angle_simu)).tolist())[:-1]                                                            # Changes (dy) in the y-coordinates for each segment of the leaf shape
    x, y = np.cumsum(dx), np.cumsum(dy)

    return x, y
