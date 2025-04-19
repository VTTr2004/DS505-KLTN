import pandas as pd
import numpy as np
import math

from dataclasses import dataclass, field
from typing import List

@dataclass
class Check:
    Active: bool = False
    Kind: int = 0
    List_Vehicle: List[int] = field(default_factory=lambda: [])
    Angle: List[float] = field(default_factory=lambda: [])

    def __add__(self, other):
        if not isinstance(other, Check):
            return NotImplemented
        return Check(
            Active=self.Active,
            Kind=self.Kind,
            List_Vehicle = self.List_Vehicle + other.List_Vehicle,
            Angle = self.Angle + other.Angle
            )

    def __repr__(self):
        return f"Check({self.Active}, {self.Kind}, {self.List_Vehicle}, {self.Angle})"
    


class Map:

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

    def __init__(self, col, row, char, checker):
        self.i = 0
        self.Active = False
        self.Traffict_Light = False
        self.Img_ID = 0

        # Char = [class_ID, color_feature, box]
        self.Dict_char = {}

        self.List_Checker = np.array([[Check()  for _ in range(col)] for _ in range(row)])
        
        # contanst
        self.col = col
        self.row = row
        self.Char = char
        self.Check = checker

    def Active_On(self, ID):
        if self.Img_ID >= ID:
            self.Active = True

    def Light_On(self):
        self.Traffict_Light = True

    def GetListChar(self):
        # char = [class_id, color_feature, box, lost, Px_Py, errors]
        return self.Dict_char


    #-------------------Main---------------#
    def UpdateData(self, chars, amount_ID = 150):
        # char = {class_ID : [], 
        #         colorfeature : [],
        #         box : []}
        if len(chars) == 0:
            return

        for k in list(self.Dict_char.keys()):
            if len(chars) == 0:
                break
            self.Char.Read_Char(self.Dict_char[k])
            if self.Char.CheckLost(30):
                chars = self.Char.IsChar(chars, self.Img_ID)
                self.Dict_char[k] = self.Char.GetData(ForCheck = False)
            else:
                del self.Dict_char[k]
        for char in chars:
            self.Dict_char[self.i] = list(char) + [0, [-1., -1], []]
            self.i += 1

        if self.i >= amount_ID:
            self.Active = True
        if ~self.Active:
            for char in self.Dict_char.values():
                self.Char.Read_Char(char)
                # if self.Char.Check_Active:
                try:
                    box = self.Char.GetMatrix(self.row, self.col)
                    check_temp = Check(*[False] + self.Char.GetData())
                    self.List_Checker[box[0][0]:box[0][1], box[0][2]:box[0][3]] += check_temp
                    self.List_Checker[box[1][0]:box[1][1], box[1][2]:box[1][3]] += check_temp
                except:
                    print(char)
                    break
            return 

        self.Img_ID += 1
        if self.Img_ID % 30 != 0:
            return
        for k in self.Dict_char.keys():
            self.Char.Read_Char(self.Dict_char[k])
            address = self.Char.GetIDChecker()
            list_error = self.List_Checker[address[0], address[1]].CheckError(self.Char)
            self.Char.ReadError(list_error)
            self.Dict_char[k] = self.Char.GetData(ForCheck = False)
        self.Img_ID = 0
        return 