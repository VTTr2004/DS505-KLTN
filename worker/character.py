import numpy as np
import math

class Character:
  # def __init__(self) -> None:
  #   self.cls_id = -1
  #   self.feature_color = [-1, -1, -1] # Use Mean HSV
  #   self.feature_point = [-1, -1, -1] # [X_center, Y_center, w, h]
  #   self.speed = [0, 0, 0, 0] # [V_x, V_y, V_w, V_h]
  #   self.lost = 0
  #   self.violate = 0

  def Read_Char(self, input: list) -> None:
    # input = [cls_id, <ft_color>, <ft_point>, <speed>, lost, violate]
    self.cls_id = int(input[0])
    self.feature_color = input[1:4]
    self.feature_point = input[4:8]
    self.speed = input[8:12]
    self.lost = input[12]
    self.violate = input[13]

  def Check_Lost(self, num_lost: int) -> bool:
    return True if self.lost >= num_lost + 1 else False

  def Get_Cls(self) -> int:
    return self.cls_id
  
  @staticmethod
  def Get_Cos(angle_deg) -> int:
    if angle_deg == 90 or angle_deg == 270:
      return 0
    return np.cos(np.radians(angle_deg))
  
  @staticmethod
  def Get_Sin(angle_deg) -> int:
    if angle_deg == 0 or angle_deg == 180:
      return 0
    return np.sin(np.radians(angle_deg))

  def Get_Direction(self) -> list[float]:
    speed = self.speed[:2]
    dis = np.sqrt(speed[0]**2 + speed[1]**2)
    if dis <= 3:
      return [0, 0]
    deg = math.degrees(math.atan2(speed[1], speed[0])) % 360
    deg = int(round(deg, 0))
    return [Character.Get_Cos(deg), Character.Get_Sin(deg)]


  def Get_Point_Future(self, lecay: float) -> list:
    temp = np.array(self.feature_point)
    temp += (self.lost + 1) * lecay * np.array(self.speed)
    return temp.tolist()

  def Get_ID_Check(self):
    return int((self.feature_point[0] - self.speed[0]) / 40), int((self.feature_point[1] - self.speed[1]) / 40)

  def Data_For_reID(self) -> list:
    ft_point = self.Get_Point_Future(0.9)
    return [self.cls_id] + self.feature_color + ft_point + self.speed + [self.lost, self.violate]

  '''
  input = [cls_id, ft_color_1, ft_color_2, ft_color_3, X_cen, Y_cen, w, h]
  '''
  @staticmethod
  def New_Char(input: list) -> list:
    return input + [0, 0, 0, 0, 0, 0] # thêm speed, lost và violate