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

    def __init__(self, h_img, w_img, col, row, char, checker):
        self.Active = False
        self.Traffict_Light = False
        self.Img_Now = None # is a numpy array
        self.Img_ID = 0

        # Char = [class_ID, color_feature, box]
        self.List_Char = {} # is dict

        self.List_Checker = np.array([[Check()  for _ in range(col)] for _ in range(row)])
        
        # contanst
        self.h_img = h_img
        self.w_img = w_img
        self.col = col
        self.row = row
        self.Char = char
        self.Check = checker

    def Active_On(self, ID):
        if self.Img_ID >= ID:
            self.Active = True

    def Light_On(self):
        self.Traffict_Light = True

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
            for char in self.List_Char:
                self.Char.Read_Char(char)
                box = self.Char.GetMatrix(self.row, self.col)
                check_temp = Check(*[False] + self.GetData())
                self.List_Checker[box[0][0]:box[0][1], box[0][2]:box[0][3]] += check_temp
                self.List_Checker[box[1][0]:box[1][1], box[1][2]:box[1][3]] += check_temp
            return 

        for char in self.List_Char:
            self.Char.Read_Char(char)
            address = self.Char.GetIDChecker()
            list_error = self.List_Checker[address[0], address[1]].CheckError(char)
            self.Char.ReadError(list_error)

        return
    