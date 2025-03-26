import Def_common


class Character:
    def __init__(self, box_1, box_2):
        # box = [label, x_min, y_min, x_max, y_max]

        self.box_1 = box_1
        self.box_2 = box_2

    def Center(self):
        _, x_1, y_1, x_2, y_2 = self.box_1

        return [(x_1 + x_2) / 2, (y_1 + y_2) / 2]
    
    def Value(self, kind = "all"):
        # 

        if kind == 'b_1':
            return self.box_1
        if kind == 'b_2':
            return self.box_2
        if kind == 'center':
            return self.Center()
        if kind == 'vehicle':
            return self.box_1[0]
        if kind == 'rotation':
            return Def_common.Cal_Angle(self.box_1[1], self.box_1[2], self.box_2[1], self.box_2[2])
        if kind == 'distance':
            return Def_common.Cal_Dis(self.box_1[1], self.box_1[2], self.box_2[1], self.box_2[2])

        return self.vehicle
    
    