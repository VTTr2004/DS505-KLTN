import math
import numpy as np


ANGLE_KIND = np.array([0., 45., 90., 135., 180., 225., 270., 315.])
DIS_ANGLE = 22.5


def Cal_Angle(x_1, y_1, x_2, y_2):
        # Get angle of line with Ox

        dx = x_2 - x_1
        dy = y_2 - y_1
        angle_rad = math.atan(dy, dx)

        return (math.degrees(angle_rad) + 360) % 360

def Cal_Dis(x_1, y_1, x_2, y_2):
    # Get distance from point_1 and point_2

    dx = (x_1 - x_2) ** 2
    dy = (y_1 - y_2) ** 2
        
    return math.sqrt(dx + dy)

def Kind_Angle(angle):
    # Get angle_begin & angle_end

    p_min = np.argmin(ANGLE_KIND - angle)
    result = [ANGLE_KIND[p_min] - DIS_ANGLE, ANGLE_KIND[p_min] + DIS_ANGLE]
    
    if p_min % 2 == 1:
        return [result[0] - 45, result[1] + 45]
    return result