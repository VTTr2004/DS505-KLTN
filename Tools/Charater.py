import Def_common

#---------------Character---------------#
class Character:
    def __init__(self, box_1, box_2):
        # box = [label, x, y]

        self.vehicle = box_1[0]
        self.x_1 = box_1[1]
        self.y_1 = box_1[2]
        self.x_2 = box_2[1]
        self.y_2 = box_2[2]
    
    def Value(self, kind = "all"):
        # 

        if kind == 'p_1':
            return [self.x_1, self.y_1]
        if kind == 'p_2':
            return [self.x_2, self.y_2]
        if kind == 'rotation':
            return Def_common.Cal_Angle(self.x_1, self.y_1, self.x_2, self.y_2)
        if kind == 'distance':
            return Def_common.Cal_Dis(self.x_1, self.y_1, self.x_2, self.y_2)

        return self.vehicle
    
    