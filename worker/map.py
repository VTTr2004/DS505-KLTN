import pandas as pd
import numpy as np
import cv2
import pickle
from scipy.optimize import linear_sum_assignment
from worker.character import Character
from worker.checker import Checker
from worker.drawer import Draw

class Map:
  lb_dict = {
      3 : 'nguoi di bo',
      4 : 'xe may',
      5 : 'Oto',
      6 : 'Xe cho hang nho',
      7 : 'Xe cho hang nho',
      8 : 'Xe khach'
  }

  def __init__(self) -> None:
    self.name = None
    self.check_reader = Checker()
    self.char_reader = Character()
    self.cam = None

  def Load_Map(self, cam: str) -> None:
    self.name = cam
    with open(f"./infor/map/{cam}.pkl", 'r') as file:
      self.cam = pickle.load(file)

  def Active(self, num_img = 1800) -> None: # Khoảng 60s
    if self.cam.img_id >= num_img:
      return True
    False

  def Save_Map(self) -> None:
    with open(f"./infor/map/{self.name}.pkl", 'wb') as file:
      pickle.dump(self.cam, file)


  #------------------------------------------MainOfMap
  '''
  char = [cls_id, ft_color_1, ft_color_2, ft_color_3, X_cen, Y_cen, w, h]
  '''
  @staticmethod
  def Cal_Matrix(char_old: list, char_new: list):
    result = np.linalg.norm(np.array(char_old)[:, None, :] - np.array(char_new)[None, :, :], axis=2)
    return result

  def Re_ID(self, char_old: list, char_new: list) -> list:
    size_old = len(char_old)
    size_new = len(char_new)
    size = max(size_old, size_new)

    matrix = self.Cal_Matrix(char_old, char_new)
    matrix_padded = np.full((size, size), fill_value = 1e9)
    matrix_padded[:size_old, :size_new] = matrix

    old_ind, new_ind = linear_sum_assignment(matrix_padded)
    result = [[], []]
    for i, j in zip(old_ind, new_ind):
      if i < size_old and j < size_new:
        result[0].append(i)
        result[1].append(j)

    return result[0], result[1]

  def Re_Infor(self, char_old: list, char_new: list) -> None:
    old_id, new_id = self.Re_ID(char_old, char_new)

    char_old = np.array(char_old)
    char_new = np.array(char_new)

    # Fix speed
    char_old[old_id, 8: 12] = char_new[new_id, 4: 8] - char_old[old_id, 4: 8]
    # Fix value
    char_old[old_id, :8] = char_new[new_id]

    # add lost
    char_old[[i not in old_id for i in range(len(char_old))], -1] += 1

    # add new char
    char_new = [self.read_charer.New_Char(char) for char in char_new[[i not in new_id for i in range(len(char_new))]]]
    char_old = np.vstack((char_old, char_new))

    self.cam.chars = char_old.tolist()

  def Active_False(self):
    for char in self.cam.chars:
      self.char_reader.Read_Char(char)
      angle = self.char_reader.Get_Angle
      if angle:
        check_x, check_y = self.Get_ID_Check
        lb = self.Get_Cls
        self.cam.map[check_x][check_y][0].append(angle)
        self.cam.map[check_x][check_y][1].append(lb)
    self.cam.img_id += 1
    if self.cam.img_id >= 1500:
      self.cam.map = [[self.check_reader.Create_Angle(val[0]) + self.char_reader.Creat_Vehicle(val[1])
                       for val in col]
                       for col in self.cam.map]

  def Active_True(self):
    chars = np.array(self.cam.chars)
    img = cv2.imread(f"./infor/img/{self.name}.jpg")
    for char in chars:
      check_x, check_y = self.Get_ID_Check
      self.check_reader.Read_Checker(self.cam.map[check_x][check_y])
      temp = self.check_reader.Checker_Error(chars)
      if temp:
        img = Draw.DrawFromMap(img, char)
    cv2.imwrite(f"./infor/img/{self.name}.jpg", img)

  def Run(self, input: list) -> None:
    self.cam.img_id += 1
    if len(input) == 0:
      return

    chars = []
    for char in self.cam.chars:
      self.char_reader.Read_Char(char)
      if self.char_reader.Check_Lost(150): # khoảng 5 giây
        continue
      chars.append(self.char_reader.Data_For_reID)

    self.Re_Infor(chars, input)

    if self.Active() and self.cam.img_id % 10 == 0:
      self.Active_True
      return 
    self.Active_False
    return