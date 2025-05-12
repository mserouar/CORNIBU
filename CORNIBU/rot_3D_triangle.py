import numpy as np

def rot_3D_triangle(xyz,rotangle) :

# Inputs:

# xyz:
# Type: NumPy array (matrix)
# Description: A [n 9] matrix of coordinates of n triangles defined by their 3 points [X1 Y1 Z1 X2 Y2 Z2 X3 Y3 Z3].

# rotangle:
# Type: NumPy array (matrix)
# Description: A 3-element matrix for rotation angles, representing rotation about x, y, and z axes respectively.

# Output:

# xyz:
# Type: NumPy array (matrix)
# Description: The rotated matrix of coordinates.

    try :
        xyz= (xyz.reshape(3,3).transpose()) 
    except : 
        sha = int((xyz.shape[0]* xyz.shape[2])/3)
        xyz= (xyz.reshape(sha,3).transpose())

    ax=rotangle[0]/180*np.pi
    ay=rotangle[1]/180*np.pi
    az=rotangle[2]/180*np.pi

    bx = [[1,0,0], 
        [0, np.cos(ax), np.sin(ax)],
        [0, -np.sin(ax), np.cos(ax)]]

    by = [[np.cos(ay), 0,  -np.sin(ay)], 
        [0, 1, 0],
        [ np.sin(ay) ,0 ,np.cos(ay)]]

    bz = [[np.cos(az) ,np. sin(az), 0], 
                [-np.sin(az), np.cos(az), 0],
                [ 0, 0,  1]]

    B = np.asarray(bx)@np.asarray(by)@np.asarray(bz)
    xyz= np.dot(B,xyz)
    n=len(xyz[:,2])
    xyz = (xyz.transpose().flatten()) 

    return xyz
