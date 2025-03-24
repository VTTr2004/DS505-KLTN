import Def_common
from Checker import Checker
import pandas as pd
import numpy as np



def Create_Point_Char(x_1, y_1, x_2, y_2):
    pass

#---------Map---------#
class Map:
    def __init__(self, h_cam, w_cam, row : int, col : int):
        self.map = np.array([[None for c in range(col)] for r in range(row)])
        self.ratio = [h_cam / row, w_cam / col]

    def Get_Id_Checker(self, x, y):
        # Get id of checker

        # x // w_map, y // h_map
        return [x // self.ratio[1], y // self.ratio[0]]

    def Create_Checker(self, obj_list : list):
        # each obj [id, label, x, y]

        id_list = {char[0] for char in obj_list}
        df = pd.DataFrame(obj_list, columns = ["Id", "Label", "X", "Y"]).set_index("Id")

        # Init and Update checker
        for id in id_list:
            df_id = df.loc[[id]]
            num = df_id.shape[0]
            for i in range(0, num - 1):
                lb = df_id.iloc[i, 1].values
                x_1, y_1 = df_id.iloc[i, -2:].values
                x_2, y_2 = df_id.iloc[i + 1, -2:].values

                id_check_bg = self.Get_Id_Checker(x_1, y_1)
                id_check_end = self.Get_Id_Checker(x_2, y_2)

                angle = Def_common.Cal_Angle(x_1, y_1, x_2, y_2)
                for id_r in range(id_check_end[0], id_check_end[0]):
                    for id_c in range(id_check_bg[1], id_check_end[1]):
                        if self.map[id_r, id_c] is None:
                            self.map[id_r, id_c] = Checker(angle, [lb])
                        else:
                            self.map[id_r, id_c].Add_Exp(angle, [lb])

        # self-define checker
        h_map, w_map = self.map.shape
        for h in h_map:
            for w in w_map:
                self.map[h, w].Define_Self
                

        return 0