import Def_common
import numpy as np

#-------------Checker-------------#
class Checker:

    def __init__(self, rotation, veh_list, kind = -1):
        self.value_dict = {
            "Street" : kind,
            "Rotation" : np.array(rotation),
            "Vehicle" : veh_list
        }

    def Add_Exp(self, rotation, veh_list):
        #

        self.value_dict["Rotation"] += np.array(rotation)
        self.value_dict["Vehicle"] += veh_list

    def Define_Self(self):
        # self-definition

        num = len(self.value_dict["Vehicle"])
        id_vehicle = set(self.value_dict["Vehicle"])
        ratio = 1 / len(id_vehicle)

        #---------Vehicle---------#  
        v_list = []
        for id in id_vehicle:
            if self.value_dict["Vehicle"].count(id) / num >= ratio:
                v_list.append(id)
        self.value_dict["Vehicle"] = v_list

        #---------Rotation---------#
        self.value_dict["Rotation"] /= num

    