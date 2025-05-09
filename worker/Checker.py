import numpy as np

class Checker:

  lb_dict = {
      3 : 'nguoi di bo',
      4 : 'xe may',
      5 : 'Oto',
      6 : 'Xe cho hang nho',
      7 : 'Xe cho hang nho',
      8 : 'Xe khach'
  }
  def __init__(self) -> None:
    self.angle = [0, 0]
    self.vehicle = []
    self.char_reader = Character()

  def Read_Checker(self, check: list) -> None:
    self.angle = check[:2]
    self.vehicle = check[2:]
  #--------------------DefineCheck
  @staticmethod
  def Create_Angle(input: list) -> list:
    temp = np.array(input)
    Q1 = np.percentile(temp, 25)
    Q3 = np.percentile(temp, 75)
    if Q3 - Q1 > 190:
      temp = np.array([i if i < 180 else i - 360 for i in temp])
      Q1 = np.percentile(temp, 25)
      Q3 = np.percentile(temp, 75)
    return [Q1, Q3]

  @staticmethod
  def Creat_Vehicle(input: list) ->list:
    result = []

    num = len(input)
    vehicle_set = set(input)
    max = 0
    temp_dict = {}
    for v in vehicle_set:
      if Checker.lb_dict[v] != 'nguoi di bo':
          temp = input.count(v)
          temp_dict[v] = temp
          max = temp if temp > max else max
      else:
          num -= input.count(v)

    for v in vehicle_set:
      if max - temp_dict[v] <= 0.5 * max:
          result.append(v)

    return result

  #--------------------CheckError
  def Wrong_Lane(self) -> bool:
    if self.char_reader.Get_Cls not in self.vehicle:
      return True
    return False

  def Wrong_trend(self) -> bool:
    angle_char = self.char_reader.Get_Angle()

    if self.angle[0] < 0 and self.angle[1] > 0:
      if 360 + self.angle[0] <= angle_char and angle_char <= 360:
        return False
      if 0 <= angle_char and angle_char <= self.angle[1]:
        return False

    if self.angle[0] <= angle_char and angle_char <= self.angle[1]:
      return False

    return True

  def Checker_Error(self, char: list) -> list:
    self.char_reader.Read_Char(char)
    result = []

    if self.Wrong_Lane():
      result.add(0)
    if self.Wrong_trend():
      result.add(1)

    return result