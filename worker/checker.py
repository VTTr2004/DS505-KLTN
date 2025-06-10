import numpy as np
from collections import Counter
from worker.character import Character

class Checker:
  def __init__(self) -> None:
    self.active = False
    self.img_ids = []
    self.angles = []
    self.vehicle = []
    self.char_reader = Character()
    
  def Read_Checker(self, check: list) -> None:
    # check = [True, [...], [...], [...]]
    self.active = check[0]
    self.img_ids = check[1]
    self.angles = check[2]
    self.vehicle = check[3]

  def Save(self):
    result = []
    result.append(self.active)
    result.append(self.img_ids)
    result.append(self.angles)
    result.append(self.vehicle)
    return result
  
  #--------------------method_active  
  @staticmethod
  def Check_Direct(direct_1, direct_2, value = 0.35, type = 'Check'):
    x_1 = direct_1[0]
    y_1 = direct_1[1]
    x_2 = direct_2[0]
    y_2 = direct_2[1]

    if type == 'Check':
      dis = np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)
      return True if dis <= value else False
    if type == 'Avg':
      x_1 = x_1*0.9 + x_2*0.1
      y_1 = y_1*0.9 + y_2*0.1
      return [x_1, y_1]
  @staticmethod
  def Define_Veh(vehs: list) -> list:
    if not vehs:
        return []
    count = Counter(vehs)
    total = len(vehs)
    ratio_dict = {veh: freq / total for veh, freq in count.items()}
    max_ratio = max(ratio_dict.values())
    result = [veh for veh, ratio in ratio_dict.items() if ratio / max_ratio >= 0.6]
    return result

  def Active_False(self, img_id, char: list) -> list:
    self.char_reader.Read_Char(char)
    cls_id = self.char_reader.Get_Cls()
    char_angle = self.char_reader.Get_Direction()
    if len(self.angles) == 0:
      self.angles.append(char_angle)
      self.vehicle.append([cls_id])
    else:
      if Checker.Check_Direct(self.angles[-1], char_angle):
        self.angles[-1] = Checker.Check_Direct(self.angles[-1], char_angle, type = 'Avg')
        self.vehicle[-1].append(cls_id)
      else:
        self.img_ids.append(img_id)
        if Checker.Check_Direct(self.angles[0], char_angle):
          self.active = True
          temp = self.img_ids[-1] if len(self.img_ids) > 0 else 0
          if img_id - temp <= 5:
            # Trường hợp xe đi ngược chiều
            self.active = False
            self.img_ids.pop()
            self.img_ids.pop()
            self.angles.pop()
            self.vehicle.pop()
        else:
          # Trường hợp đường trên 3 hướng
          self.angles.append(char_angle)
          self.vehicle.append([cls_id])
    if self.active:
      for i in range(len(self.vehicle)):
        self.vehicle[i] = Checker.Define_Veh(self.vehicle[i])
    if len(self.img_ids) == 0 and img_id >= 120:
      # Trường hợp đường chỉ có 1 hướng
      self.active = True
    if len(self.img_ids) != 0 and img_id - self.img_ids[-1] >= 120:
      self.active = True
    return char
  
  def Active_True(self, img_id, char: list) -> list:
    if self.Checker_Error(img_id % self.img_ids[-1], char):
      char[-1] = 1
    return char
  
  def Run(self, img_id, char: list) -> list:
    if self.active:
      return self.Active_True(img_id, char)
    else:
      return self.Active_False(img_id, char)

  #----------------Check_Error
  def Get_Code_Id(self, img_id):
    img_id = img_id % self.img_ids[-1]
    temp = 0
    for id in self.img_ids:
      if img_id > id:
        temp += 1
      else:
        break
    return temp
  
  def Checker_Error(self, img_id, char: list) -> list:
    self.char_reader.Read_Char(char)
    img_id = self.Get_Code_Id(img_id)

    if self.Wrong_Lane(id) or self.Wrong_Trend(id):
      return True
    return False
  
  def Wrong_Lane(self, id) -> bool:
    # Lỗi lấn làn
    if self.char_reader.Get_Cls() not in self.vehicle[id]:
      return True
    return False
  def Wrong_Trend(self, id) -> bool:
    # Lỗi ngược chiều, vượt đèn đỏ
    char_angle = self.char_reader.Get_Direction()
    return Checker.Check_Direct(self.angles[id], char_angle)