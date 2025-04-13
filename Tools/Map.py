import pandas as pd
import numpy as np
import math

#---------Map---------#
class Map:

    class Character:
        # Process Object #
        def __init__(self):
            self.Kind = -1
            self.Box_After  =  [-1, -1, -1, -1] # [x, y, w, h]
            self.Box_Now    =  [-1, -1, -1, -1] # [x, y, w, h]

        def Read_Char(self, data):
            self.Kind = data[0]
            self.Box_Now = data[-1]
            if len(data) == 4:
                self.Box_After = data[-2]

        def GetAngel(self):
            # Get angle create by char and Ox (-)

            d_x = self.Box_Now[0] - self.Box_After[0]
            d_y = self.Box_Now[1] - self.Box_After[1]

            angle = math.degrees(math.atan2(d_y, d_x)) + 360

            return angle % 360
        
        def GetSpeed(self):
            d_x = self.Box_Now[0] - self.Box_After[0]
            ratio = d_x / self.Box_Now[3]

            angle = self.GetAngel() % 180
            if 45 <= angle or angle < 135:
                d_y = self.Box_Now[1] - self.Box_After[1]
                ratio = d_y / self.Box_Now[3]
                
            return ratio
        

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

        # Char = [kind, box_1, box_2]
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