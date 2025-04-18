import pandas as pd
import numpy as np

class Checker:


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

    def ChooseVehicle(self, data, lb_dict):
        # Choose Vehicle
        result = []

        num = len(data)
        vehicle_set = set(data)
        max = 0
        temp_dict = {}
        for v in vehicle_set:
            if self.lb_dict[v] != 'nguoi di bo':
                temp = data.count(v)
                temp_dict[v] = temp
                max = temp if temp > max else max
            else:
                num -= data.count(v)

        for v in vehicle_set:
            if max - temp_dict[v] <= 0.5 * max:
                result.append(v)

        return result
    
    def CreateAngle(self, data):
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
        char_lb = char.GetClassID()

        # People #
        if self.lb_dict[char_lb] == 'nguoi di bo':
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