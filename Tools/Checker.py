import Def_common
import numpy as np

#-------------Checker-------------#
class Checker:

    def __init__(self, rotation : list, veh_list : list, kind = -1):
            self.street = kind,
            self.rotation = rotation,
            self.vehicle = veh_list

    def Add_Val(self, rotation : list, veh_list : list):
        #

        self.rotation += rotation
        self.rotation += veh_list

    def Define_Self(self):
        # self-definition

        num = len(self.vehicle)
        id_vehicle = set(self.vehicle)
        ratio = 1. / len(id_vehicle)

        #---------Vehicle---------#  
        v_list = []
        for id in id_vehicle:
            if self.vehicle.count(id) / num >= ratio:
                v_list.append(id)
        self.vehicle = v_list

        #---------Rotation---------#
        

    