

def triangle_area(x1, x2, x3, y1, y2, y3, z1, z2, z3):

# Inputs:

# x1, x2, x3, y1, y2, y3, z1, z2, z3:
# Type: Float
# Description: Coordinates of the vertices of the triangle.

# Output:

# area:
# Type: Float
# Description: The area of the triangle.

    ux, uy, uz = x2-x1, y2-y1, z2-z1
    vx, vy, vz = x3-x1, y3-y1, z3-z1
    cx, cy, cz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    magnitude = (cx**2 + cy**2 + cz**2)**0.5
    return 0.5 * magnitude

