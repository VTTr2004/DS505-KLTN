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

def Code_Angle(angle):
    # Get code,

    p_min = np.argmin(ANGLE_KIND - angle)
    return p_min

def Check_Angle(angle, code):
    # Get angle_begin & angle_end

    result = [ANGLE_KIND[code] - DIS_ANGLE, ANGLE_KIND[code] + DIS_ANGLE]
    if code % 2 == 1:
        result = [result[0] - 45, result[1] + 45]
    
    return True if result[0] <= angle and angle <= result[1] else False

def Get_Q1Q3(speed_list):
    #

    temp = np.array(speed_list)
    Q1 = np.percentile(temp, 25)
    Q3 = np.percentile(temp, 75)

    return [Q1, Q3]