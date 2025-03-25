import Def_common
import numpy as np

#-------------Checker-------------#
class Checker:

    def __init__(self, kind = -1):
        self.street = kind,
        self.rotation_count = [0] * 8,
        self.rotation_flag = [False] * 8
        self.speed = []
        self.vehicle = []

    def Add_Val(self, rotation : list, veh_list : list, speed_list : list):
        #

        self.speed += speed_list
        self.vehicle += veh_list

        for angle in rotation:
            kind_angle = Def_common.Code_Angle(angle)
            self.rotation_count[kind_angle] += 1
  

    def Define_Self(self):
        # self-definition

        num = len(self.vehicle)
        id_vehicle = set(self.vehicle)
        ratio = 1. / len(id_vehicle)

        #----------speed----------# 
        self.speed = Def_common.Get_Q1Q3(self.speed)

        #---------Vehicle---------#  
        self.vehicle = [id for id in set(self.vehicle) if self.vehicle.count(id) / num >= ratio]

        #---------Rotation---------#
        num_k_angle = sum(1 for x in self.rotation_count if x > 0) or 1
        for i in range(8):
            if self.rotation_count[i] / num >= 1. / num_k_angle:
                self.rotation_flag[i] = True
        self.rotation_count = [0] * 8

    def Check_Char(self, char):
        #

        result = []

        rotation_char = char.Value(kind = "rotation")
        kind_angle = Def_common.Code_Angle(rotation_char)
        vehicle_char = char.Value(kind = "vehicle")
        speed_char = char.Value(kind = "distance")

        # wrong line
        if vehicle_char not in self.vehicle:
            result.append(0)

        # wrong rotation
        if not self.rotation_flag[kind_angle]:
            result.append(1)

        # over speed
        if self.speed[1] < speed_char:
            result.append(2)

        return result