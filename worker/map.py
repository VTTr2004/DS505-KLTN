import pandas as pd
import numpy as np
import cv2
import pickle
from scipy.optimize import linear_sum_assignment
from worker.character import Character
from worker.checker import Checker
from worker.drawer import Draw

class Map:
  def __init__(self) -> None:
    # self.name = None
    self.check_reader = Checker()
    self.char_reader = Character()
    # self.cam = None

  def Load_Map(self, cam: str) -> None:
    self.name = cam
    with open(f"./infor/map/{cam}.pkl", 'rb') as file:
      self.cam = pickle.load(file)
    return 

  def Active(self, num_img = 1800) -> None: # Khoảng 60s
    if self.cam.img_id >= num_img:
      return True
    False

  def Save_Map(self) -> None:
    with open(f"./infor/map/{self.name}.pkl", 'wb') as file:
      pickle.dump(self.cam, file)


  #------------------------------------------MainOfMap
  '''
  char = [cls_id, *ft_color, *point, *speed, lost, violate]
  trong đó:
  ft_color = [ft_color_1, ft_color_2, ft_color_3]
  point = [x, y, w, h]
  speed = [spd_x, spd_y, spd_w, spd_h]
  len(char) = 14
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
      if i < size_old and j < size_new and Map.Cal_Matrix([char_old[i]], [char_new[j]]) < 200:
        result[0].append(i)
        result[1].append(j)

    return result[0], result[1]

  def Re_Infor(self, char_old: list, char_new: list) -> None:
    if len(char_old) == 0:
      self.cam.chars = char_new
      return
    char_old = np.array(char_old)
    char_new = np.array(char_new)
    old_id, new_id = self.Re_ID(char_old[:, :8], char_new[:, :8])

    # Fix speed
    char_old[old_id, 8: 12] = char_new[new_id, 4: 8] - char_old[old_id, 4: 8]
    # Fix value
    char_old[old_id, :8] = char_new[new_id, :8]

    # add lost
    char_old[[i not in old_id for i in range(len(char_old))], 12] += 1

    # add new char
    char_new = char_new[[i not in new_id for i in range(len(char_new))]]
    char_old = np.vstack((char_old, char_new))

    self.cam.chars = char_old.tolist()

  def Run(self, input: list) -> None:
    self.cam.img_id += 1
    if len(input) == 0:
      return
    
    input = [Character.New_Char(ip) for ip in input]
    self.Re_Infor(self.cam.chars, input)

    for id in range(len(self.cam.chars)):
      self.char_reader.Read_Char(self.cam.chars[id])
      check_x, check_y = self.char_reader.Get_ID_Check()
      if len(self.cam.map[check_x][check_y]) == 0:
        self.cam.map[check_x][check_y] = Checker().Save()
      self.check_reader.Read_Checker(self.cam.map[check_x][check_y])
      self.cam.chars[id] = self.check_reader.Run(self.cam.img_id, self.cam.chars[id])
      self.cam.map[check_x][check_y] = self.check_reader.Save()
    return