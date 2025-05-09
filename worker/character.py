import numpy as np

class Character:
  def __init__(self) -> None:
    self.cls_id = -1
    self.feature_color = [-1, -1, -1] # Use Mean HSV
    self.feature_point = [-1, -1, -1] # [X_center, Y_center, w, h]
    self.speed = [0, 0, 0, 0] # [V_x, V_y, V_w, V_h]
    self.lost = 0

  def Read_Char(self, input: list) -> None:
    # input = [cls_id, <ft_color>, <ft_point>, <speed>, lost]
    self.cls_id = int(input[0])
    self.feature_color = input[1:4]
    self.feature_point = input[4:8]
    self.speed = input[8:12]
    self.lost = input[12]

  def Check_Lost(self, num_lost: int) -> bool:
    return True if self.lost >= num_lost + 1 else False

  def Save_Char(self) -> list:
    # return value for save
    return [self.cls_id] + self.feature_color + self.feature_point + self.speed + [self.lost] + self.error

  def Get_Cls(self) -> int:
    return self.cls_id

  def Get_Angle(self) -> int:
    speed = self.speed[:2]
    if speed[0] == 0 and speed[1] == 0:
      return False
    return math.degrees(math.atan2(speed[1], speed[0])) % 360

  def Get_Point_Future(self, lecay: float) -> list:
    temp = np.array(self.feature_point)
    temp += self.lost * lecay * np.array(self.speed)
    return temp.tolist()

  def Get_ID_Check(self):
    return int((self.feature_point[0] - self.speed[0]) / 40), int((self.feature_point[1] - self.speed[1]) / 40)

  def Data_For_reID(self) -> list:
    ft_point = self.Get_Point_Future
    return [self.cls_id] + self.feature_color + ft_point


  '''
  input = [cls_id, ft_color_1, ft_color_2, ft_color_3, X_cen, Y_cen, w, h]
  '''
  def Is_Char(self, input: list) -> None:
    self.cls_id = int(input[0])
    self.feature_color = input[1:4]
    self.speed = input[4:8] - self.feature_point
    self.feature_point = input[4:8]
    self.lost = 1

  @staticmethod
  def New_Char(input: list) -> list:
    return input + [0, 0, 0, 0, 1] # thêm vị trí trước và lost