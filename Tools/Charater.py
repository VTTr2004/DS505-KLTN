import pandas as pd
import numpy as np
import math 


class Character:
    # Process Object #
    def __init__(self):
        self.Class_ID = -1
        self.Color_Feature = 0 # Use HSV
        self.Box = [-1, -1, -1, -1] # [x, y, w, h]

        self.Px_Py_Before = [-1., -1.] # [X, Y]

        self.Lost = 0
        self.List_error = []

    def Check_Active(self):
        if self.Px_Py_Before != [-1., -1.]:
            return True
        return False

    def GetMatrix(self, row, col):
        box_1 = self.Px_Py_Before + self.Box[2:]
        x_min = (box_1[0] - box_1[2] / 2) * row
        x_max = (box_1[0] + box_1[2] / 2) * row
        y_min = (box_1[1] - box_1[3] / 2) * col
        y_max = (box_1[1] + box_1[3] / 2) * col
        box_1 = list(map(int, [x_min, x_max, y_min, y_max]))
        
        box_2 = self.Box
        x_min = (box_2[0] - box_2[2] / 2) * row
        x_max = (box_2[0] + box_2[2] / 2) * row
        y_min = (box_2[1] - box_2[3] / 2) * col
        y_max = (box_2[1] + box_2[3] / 2) * col
        box_2 = list(map(int, [x_min, x_max, y_min, y_max]))

        return [box_1, box_2]

    def GetClassID(self):
        return self.Class_ID
    
    def GetIDChecker(self, row, col):
        return [self.Px_Py_Before[0] * row, self.Px_Py_Before[1] * col]
    
    def CheckLost(self, num):
        if self.Lost >= num:
            return False
        return True

    def GetAngle(self):
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

    def GetData(self, ForCheck = True):
        class_id = self.Class_ID
        color = self.Color_Feature
        box = self.Box
        lost = self.Lost
        Px_Py = self.Px_Py_Before
        errors = self.List_error

        if ForCheck:
            return [class_id, color, box]
        return [class_id, color, box, lost, Px_Py, errors]

    def Read_Char(self, data):
        self.Class_ID = data[0]
        self.Color_Feature = data[1]
        self.Box = data[2]
        try:
            self.Lost = data[3]
            self.Px_Py_Before = data[4]
            self.List_error = data[5]
        except:
            pass

    def GetInfor(self):
        return [0, [self.Class_ID - 3], [self.GetAngle]]

    def CheckMotion(self, box, ratio):
        # box is being Series for each is [x, y, w, h]

        x_min = self.Box[0] - self.Box[2] / 2
        y_min = self.Box[1] - self.Box[3] / 2
        x_max = self.Box[0] + self.Box[2] / 2
        y_max = self.Box[1] + self.Box[3] / 2
        box_1 = np.array([x_min, y_min, x_max, y_max])
        area_box_1 = self.Box[2] * self.Box[3]
        
        # box
        box = np.array(box.values.tolist()).reshape(-1, 4)
        box = pd.DataFrame(box, columns = ['x', 'y', 'w', 'h'])

        box['x_min'] = (box['x'] - box['w'] / 2).clip(lower=box_1[0])
        box['y_min'] = (box['y'] - box['h'] / 2).clip(lower=box_1[1])
        box['x_max'] = (box['x'] + box['w'] / 2).clip(upper=box_1[2])
        box['y_max'] = (box['y'] + box['h'] / 2).clip(upper=box_1[3])

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

    def IsChar(self, datas, img_id):
        # data = [class_ID, color_feature, box]
        if len(datas) == 0:
            return datas
        
        class_ids = []
        boxes = []
        color_features = []

        for d in datas:
            class_ids.append(d[0])
            color_features.append(d[1])
            boxes.append(d[2])

        datas = pd.DataFrame({
            'class_ID': class_ids,
            'color_feature': color_features,
            'box': boxes
        })
        ratio = 0.7
        ID_check = np.array(datas['class_ID'] == self.Class_ID)
        Color_check = np.array(self.CheckColorFeature(datas['color_feature'].tolist(), ratio))
        # Motion_Check = np.array(self.CheckMotion(datas['box'], ratio))
        
        final_mask = ID_check & Color_check 

        char_true = datas[final_mask].reset_index(drop=True)
        char_false = datas[~final_mask].reset_index(drop=True)

        if char_true.shape[0] == 0:
            self.Lost += 1
            return char_false.values
    
        if char_true.shape[0] >= 2:
            # Choose Char_true
            temp = np.array(self.CheckColorFeature(char_true['color_feature'].tolist(), ratio, return_score = True))
            max = np.argmax(temp)
            temp = char_true[~char_true.index.isin([max])]
            char_true = char_true.iloc[max]
            char_false = pd.concat([char_false, temp], ignore_index = True)
        if char_true.shape[0] == 1:
            # Is ID
            self.Color_Feature = char_true['color_feature'].tolist()[0]
            self.Box = char_true['box'].tolist()[0]
            if img_id % 30 == 0:
                self.Px_Py_Before = [self.Box[0], self.Box[1]]
        
        return char_false.values