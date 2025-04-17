import pandas as pd
import numpy as np
import math

#---------Map---------#
class Map:

    i = 0

    lb_dict = {
        0 : 'den do',
        1 : 'den xanh',
        2 : 'vach di bo',
        3 : 'nguoi di bo',
        4 : 'xe may',
        5 : 'Oto',
        6 : 'Xe cho hang nho',
        7 : 'Xe cho hang nho',
        8 : 'Xe khach'
    }

    class Character:
        # Process Object #
        def __init__(self):
            self.Class_ID = -1
            self.Color_Feature = 0 # Use HSV
            self.Box = [-1, -1, -1, -1] # [x, y, h, w]

            self.Lost = 0
            self.Px_Py_Before = [-1., -1.] # [X, Y]
            self.Speed = 0.
            self.Angle = 0.

        def GetID(self):
            return self.Class_ID
        
        def CheckLost(self, num):
            if self.Lost >= num:
                return False
            return True

        def GetAngel(self):
            # Get angle create by char and Ox (-)

            A = np.array(self.Px_Py_Before)
            B = np.array([self.Box[0], self.Box[1]])
            v = B - A

            return math.degrees(math.atan2(v[1], v[0])) % 360
        
        def GetSpeed(self):
            angle = self.GetAngel() % 180
            if 45 <= angle or angle < 135:
                d_y = self.Box[1] - self.Px_Py_Before[1]
                ratio = d_y / self.Box[3]
            else:
                d_x = self.Box[0] - self.Px_Py_Before[0]
                ratio = d_x / self.Box[2]
                
            return ratio

        def Read_Char(self, data):
            self.Class_ID = data[0]
            self.Color_Feature = data[1]
            self.Box = data[2]

        def CheckMotion(self, box, ratio):
            # box is being Series for each is [x, y, h, w]

            x_min = self.Box[0] - self.Box[2] / 2
            y_min = self.Box[1] - self.Box[3] / 2
            x_max = self.Box[0] + self.Box[2] / 2
            y_max = self.Box[1] + self.Box[3] / 2
            box_1 = np.array([x_min, y_min, x_max, y_max])
            area_box_1 = self.Box[2] * self.Box[3]
            
            # box
            box = np.array(box.values.tolist()).reshape(-1, 4)
            box = pd.DataFrame(box, columns = ['x', 'y', 'h', 'w'])

            box['x_min'] = (box['x'] - box['h'] / 2).clip(lower=box_1[0])
            box['y_min'] = (box['y'] - box['w'] / 2).clip(lower=box_1[1])
            box['x_max'] = (box['x'] + box['h'] / 2).clip(upper=box_1[2])
            box['y_max'] = (box['y'] + box['w'] / 2).clip(upper=box_1[3])

            box['area'] = box['h'] * box['w']
            box['inter_h'] = (box['x_max'] - box['x_min']).clip(lower=0)
            box['inter_w'] = (box['y_max'] - box['y_min']).clip(lower=0)

            area_match = (box['inter_w'] * box['inter_h']).values
            area_total = box['area'].values + area_box_1 - area_match
            IOU = area_match / area_total
                    
            return [i >= ratio for i in IOU]

        def CheckColorFeature(self, data, ratio, return_score = False):
            vec1 = np.array(self.Color_Feature)
            vec2 = np.array(data)

            dot = np.dot(vec2, vec1)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2, axis=1)
            
            if return_score:
                temp = np.where(norm1 * norm2 != 0, dot / (norm1 * norm2), 0)
                return temp
            return np.where(norm1 * norm2 != 0, dot / (norm1 * norm2) >= ratio, False)
            

        def IsChar(self, datas):
            # data = [class_ID, color_feature, box]
            datas = pd.DataFrame(datas, columns = ['class_ID', 'color_feature', 'box'])

            ID_check = np.array(datas['class_ID'] == self.Class_ID)
            Motion_Check = np.array(self.CheckMotion(datas['box'], 0.7))
            Color_check = np.array(self.CheckColorFeature(datas['color_feature'].tolist(), 0.7))

            final_mask = ID_check & Motion_Check & Color_check 

            char_true = datas[final_mask].reset_index(drop=True)
            char_false = datas[~final_mask].reset_index(drop=True)

            if char_true.shape[0] == 0:
                self.Lost += 1
                return char_false.values
        
            if char_true.shape[0] >= 2:
                # Choose Char_true
                temp = char_true.apply(lambda row: self.CheckColorFeature(row['color_feature'], 0.7, return_score = True), axis=1)
                max = np.argmax(temp)
                temp = char_true[~char_true.index.isin([max])]
                char_true = char_true.iloc[max]
                char_false = pd.concat([char_false, temp], ignore_index = True)
            if char_true.shape[0] == 1:
                # Is ID
                self.Lost = 0
                self.Px_Py_Before = [self.Box[0], self.Box[1]]
                self.Box = char_true[['x', 'y', 'h', 'w']].values.tolist()[0]
                self.Color_Feature = char_true['color_feature'].values[0]
                self.Speed = 0. # process later
                self.Angle = 0. # process later
            
            return char_false.values
        

    class Checker:
        # Process Checker #
        def __init__(self):
            self.Active = False
            self.Kind = -1 # 0 : long duong, 1 : vach di bo
            self.Vehicle = []
            self.Angle = [0., 0.]

        def ReadChecker(self, data):
            self.Active = data[0]
            if self.Active:
                self.Kind = data[1]
                self.Vehicle = data[2]
                self.Angle = data[3]

        def ChooseVehicle(data):
            # Choose Vehicle
            result = []

            num = len(data)
            vehicle_set = set(data)
            max = 0
            temp_dict = {}
            for v in vehicle_set:
                if Map.lb_dict[v] != 'nguoi di bo':
                    temp = data.count(v)
                    temp_dict[v] = temp
                    max = temp if temp > max else max
                else:
                    num -= data.count(v)

            for v in vehicle_set:
                if max - temp_dict[v] <= 0.5 * max:
                    result.append(v)

            return result
        
        def CreateAngle(data):
            # return [angle_begin, angle_end]
            result = []

            temp = np.array(data)
            Q1 = np.percentile(temp, 25)
            Q3 = np.percentile(temp, 75)
            if Q3 - Q1 > 190:
                temp = np.array([i if i < 180 else i - 360 for i in temp])
                Q1 = np.percentile(temp, 25)
                Q3 = np.percentile(temp, 75)
            result = [Q1, Q3]

            return result

        def DefineChecker(self, data, check_active):
            # After map collect data -> this return infor true then auto-analysis
            # data = [Kind, Vehicle, Angle]

            if len(data[1] < check_active):
                return [False]

            self.Kind = data[0]

            self.Vehicle = self.ChooseVehicle(data[1])

            self.Angle = self.CreateAngle(data[2])

            return [True, self.Kind, self.Vehicle, self.Angle]
        
        def ReverseDirection(self, char):
            # ID Fail : 0
            angle_char = char.GetAngle()
            if self.Angle[0] < 0:
                if 360 + self.Angle[0] <= angle_char and angle_char <= 360:
                    return False
                if 0 <= angle_char and angle_char <= self.Angle[1]:
                    return False
            else:
                if self.Angle[0] <= angle_char and angle_char <= self.Angle[1]:
                    return False
                
            return True

        def WrongLane(self, char):
            # ID Fail : 1
            char_lb = char.GetID()

            # People #
            if Map.lb_dict[char_lb] == 'nguoi di bo':
                if self.Active == False:
                    return False
                if self.Kind == 1:
                    return False
                return True
            
            # Vehicle #
            if self.Active == False:
                return True
            if char_lb not in self.Vehicle:
                return True
            return False

        def CheckError(self, char):
            result = []
            
            # reverse direction #
            if self.ReverseDirection(char):
                result.append(0)
            
            # wrong lane #
            if self.WrongLane(char):
                result.append(1)


            return result
         

    def __init__(self, img, col, row):
        self.Active = False
        self.Traffict_Light = False
        self.Img_Now = None # is a numpy array
        self.Img_ID = -1
        # self.Attach_ID = 

        # Char = [class_ID, color_feature, box]
        self.List_Char = {} # is dict

        # Checker = [Active, Kind, List_Vehicle, AngleBgEd]
        self.List_Checker = np.array([[[False, -1, [], []]  for _ in range(col)] for _ in range(row)])
        
        # contanst
        self.h_img = -1
        self.w_img = -1
        self.col = col
        self.row = row
        self.Char = Map.Character()
        self.Check = Map.Checker()

    def Active_On(self, ID):
        if self.Img_ID >= ID:
            self.Active = True

    def Light_On(self):
        self.Traffict_Light = True

    def Get_ID_Check(self, char):
        # point_before = char.
        pass


    def UpdateData(self, chars):
        # char = [class_ID, color_feature, box]
        if len(chars) == 0:
            return

        chars = np.array(chars)
        for k in self.List_Char.keys:
            self.Char.Read_Char(self.List_Char[k])
            if self.Char.CheckLost(30):
                chars = self.Char.IsChar(chars)
            else:
                del self.List_Char[k]
        for char in chars:
            self.List_Char[Map.i] = char
            Map.i += 1

        if self.Img_ID % 30 != 0:
            return
        
        # self.Active = False
        if ~self.Active:
            pass

        

        return
    