import Def_common

#---------------Character---------------#
class Character:
    def __init__(self, box_1, box_2):
        # box = [label, x, y]

        self.value_dict = {
            "Vehicle" : box_1[0],
            "Rotation" : Def_common.Cal_Angle(box_1[1], box_1[2], box_2[1], box_2[2]),
            "Distance" : Def_common.Cal_Dis(box_1[1], box_1[2], box_2[1], box_2[2])
        }
    
    def Value(self, kind = "all"):
        # 

        if kind != "all":
            return self.value_dict[kind]

        return self.value_dict
    
    