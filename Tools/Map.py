import pandas as pd
import numpy as np
import math

#---------Map---------#
class Map:

    class Character:
        # Process Object #
        def __init__(self):
            self.Class_ID = -1
            self.Color_Feature = 0
            self.Box = [-1] # [x, y, h, w]
            self.Speed = 0.
            self.Angle = 0.

        def GetAngel(self):
            # Get angle create by char and Ox (-)

            d_x = self.Box_Now[0] - self.Box_After[0]
            d_y = self.Box_Now[1] - self.Box_After[1]

            angle = math.degrees(math.atan2(d_y, d_x)) + 360

            return angle % 360
        
        def GetSpeed(self, box):
            d_x = self.Box[0] - box[0]
            ratio = d_x / self.Box[2]

            angle = self.GetAngel() % 180
            if 45 <= angle or angle < 135:
                d_y = self.Box[1] - box[1]
                ratio = d_y / self.Box[3]
                
            return ratio

        def Read_Char(self, data):
            self.Class_ID = data[0]
            self.Color_Feature = data[1]
            self.Box = data[2]

        def CheckMotion(self, box, ratio):
            x_min = self.Box[0] - self.Box[2] / 2
            y_min = self.Box[1] - self.Box[3] / 2
            x_max = self.Box[0] + self.Box[2] / 2
            y_max = self.Box[1] + self.Box[3] / 2
            box_1 = [x_min, y_min, x_max, y_max]
            
            x_min = box[0] - box[2] / 2
            y_min = box[1] - box[3] / 2
            x_max = box[0] + box[2] / 2
            y_max = box[1] + box[3] / 2
            box_2 = [x_min, y_min, x_max, y_max]

            area_box_1 = self.Box[2] * self.Box[3]
            area_box_2 = box[2] * box[3]

            # area match
            inter_x_min = max(box_1[0], box_2[0])
            inter_y_min = max(box_1[1], box_2[1])
            inter_x_max = min(box_1[2], box_2[2])
            inter_y_max = min(box_1[3], box_2[3])

            inter_w = max(0, inter_x_max - inter_x_min)
            inter_h = max(0, inter_y_max - inter_y_min)
            area_match = inter_w * inter_h

            try:
                IOU = area_match / (area_box_1 * area_box_2 - area_match)
            except:
                IOU = 0.
            
            if IOU <= ratio:
                return True
            return False


        def IsChar(self, data):
            # data = [class_ID, color_feature, box]

            if self.Class_ID != data[0]:
                return False
            if self.CheckMotion(data[2]):
                return False
            
        

    class Checker:
        # Process Checker #
        def __init__(self):
            self.Active = False
            self.Kind = -1
            self.Vehicle = []
            self.Angle = [0., 0.]

        def Read_Checker(self, data):
            self.Active = data[0]
            self.Kind = data[1]
            self.Vehicle = data[2]
            self.Angle = data[3]

        def CheckError(self, char):
            result = []
            
            return result
         

    def __init__(self, img, col, row):
        self.Active = False
        self.Traffict_Light = False
        self.Img_Now = img
        self.Img_ID = -1
        # self.Attach_ID = 

        # Char = [class_ID, color_feature, box]
        self.List_Char = [] 

        # Checker = [Active, Kind, List_Vehicle, AngleBgEd]
        self.List_Checker = [[[False, -1, [], []]  for _ in range(row)] for _ in range(col)]
        

        self.Char = Map.Character()
        self.Check = Map.Checker()

    def Active_On(self, ID):
        if self.Img_ID >= ID:
            self.Active = True

    def Light_On(self):
        self.Traffict_Light = True

    def UpdateData(self, Chars):    
        pass