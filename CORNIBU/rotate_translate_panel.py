import math

def rotate_translate_panel(x1, x2, x3, x4, y1, y2, y3, y4, z1, z2, z3, z4, angle_degrees):
    center_x = (x1 + x2 + x3 + x4) / 4
    center_y = (y1 + y2 + y3 + y4) / 4
    center_z = (z1 + z2 + z3 + z4) / 4

    x1, x2, x3, x4 = [x - center_x for x in [x1, x2, x3, x4]]
    y1, y2, y3, y4 = [y - center_y for y in [y1, y2, y3, y4]]
    z1, z2, z3, z4 = [z - center_z for z in [z1, z2, z3, z4]]

    theta = math.radians(angle_degrees)
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)

    new_x1, new_x2, new_x3, new_x4 = [cos_theta * x + sin_theta * z for x, z in zip([x1, x2, x3, x4], [z1, z2, z3, z4])]
    new_y1, new_y2, new_y3, new_y4 = y1, y2, y3, y4
    new_z1, new_z2, new_z3, new_z4 = [-sin_theta * x + cos_theta * z for x, z in zip([x1, x2, x3, x4], [z1, z2, z3, z4])]

    return new_x1 + center_x, new_x2 + center_x, new_x3 + center_x, new_x4 + center_x, new_y1 + center_y, new_y2 + center_y, new_y3 + center_y, new_y4 + center_y, new_z1 + center_z, new_z2 + center_z, new_z3 + center_z, new_z4 + center_z
    
