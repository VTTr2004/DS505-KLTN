import cv2
import numpy as np

def read_img(street_img, size_map):
  # khởi tạo giá trị của đường.
  street_feature = [[0 for _ in range(size_map)] for _ in range(size_map)]
  img = cv2.resize(street_img, (size_map, size_map))
  num = len(img)
  # gắn các giá trị vật cản (0) hoặc đường (1).
  for i in range(num):
    for j in range(num):
      street_feature[i][j] = 1 if img[i][j] > 125 else 0
  return street_feature

def read_point(point_path, size_map):
  # Lấy các giá trị cần vẽ Vật Thể lên <street_feature> (vị trí hiện tại và ở frame trước).
  result = []
  points = set()
  with open(point_path, 'r') as file:
    for p in file.read().split('\n'):
      if p == '':
        continue
      temp = list(map(float, p.split(' ')))
      result.append(temp)
      points.add(int(temp[0]))
  result = np.array(result)
  pro_result = []
  for p in points:
    boxes = result[result[:,0] == p]*size_map
    temp = [p, boxes[0][1], boxes[0][2], boxes[1][1], boxes[1][2]]
    pro_result.append(list(map(int, temp)))
  return np.array(pro_result)

def get_angle_between_points(x1, y1, x2, y2):
  # Xác định hướng đi của Vật Thể thỏa điều kiện (có vị trí hiện tại và frame trước).
  dx = x2 - x1
  dy = y2 - y1
  angle_rad = np.arctan2(dy, dx)
  angle_deg = np.rad2deg(angle_rad)
  return angle_deg
def get_direction_from_angle(angle_deg, step_size=2):
  # Trả về độ giá trị thay đổi của tọa độ (dx, dy) (-2<=dx,dy<=2).
  angle_rad = np.deg2rad(angle_deg)
  dx = np.cos(angle_rad) * step_size
  dy = np.sin(angle_rad) * step_size
  return int(round(dx)), int(round(dy))
def cal_trend(come, to, points, step_size=2):
  # Lấy giá trị hướng di chuyển của Vật Thể.
  box_come = list(points[points[:,0] == come, 1:])[0]
  box_to = list(points[points[:,0] == to, 1:])[0]
  x1 = int((box_come[0]+box_come[2])/2)
  y1 = int((box_come[1]+box_come[3])/2)
  x2 = int((box_to[0]+box_to[2])/2)
  y2 = int((box_to[1]+box_to[3])/2)
  angle = get_angle_between_points(x1,y1,x2,y2)
  dx, dy = get_direction_from_angle(angle, step_size)
  return [dx, dy, to]

def read_way(way_path, points):
  # Đọc các giá trị hướng đi của đường.
  result = {}
  with open(way_path, 'r') as file:
    for way in file.read().split('\n'):
      temp = way.split(',')
      code_point = int(temp[0])
      dict_temp = {}
      dict_temp['code_situation'] = int(temp[1])
      dict_temp['gate_in'] = int(temp[2])
      dict_temp['true_trend'] = [cal_trend(code_point, int(p), points) for p in temp[3].split('-')] if temp[3] != '' else []
      dict_temp['false_trend'] = [cal_trend(code_point, int(p), points) for p in temp[4].split('-')] if temp[4] != '' else []
      result[code_point] = dict_temp
  return result

def bresenham_line(x0, y0, x1, y1):
    # Tìm các điểm nằm trên đường thẳng nối liền 2 điểm cần tìm.
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    points_x = []
    points_y = []
    if dx > dy:
        err = dx // 2
        while x != x1:
            points_x.append(x)
            points_y.append(y)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy // 2
        while y != y1:
            points_x.append(x)
            points_y.append(y)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points_x.append(x1)
    points_y.append(y1)
    return points_x, points_y

def draw_point(street_feature, points):
  # Thay đổi giá trị nằm giữa 2 điểm thành giá trị ở 2 điểm đó.
  size = len(street_feature)
  for p in points:
    x1,y1,x2,y2 = p[1:]
    for dx, dy in [[0,0],[0,1],[1,0]]:
      if max(size-1,x1+dx, y1+dy, x2+dx, y2+dy) >= size or min(x1+dx, y1+dy, x2+dx, y2+dy,0) < 0:
        continue
      xs, ys = bresenham_line(x1+dx, y1+dy, x2+dx, y2+dy)
      street_feature[xs,ys] = p[0] + 2

def handle(img_path, point_path, way_path, size = 64):
  street_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
  # Đọc Thông Số Của Bản Đồ.
  street_feature = np.array(read_img(street_img, size)).T
  street_feature = street_feature.astype('uint8')
  points = read_point(point_path, size) # thông số của các điểm đặc biệt (nơi xuất hiện, góc rẽ, ...).
  draw_point(street_feature, points, size)
  ways = read_way(way_path, points) # hướng đi của các góc, nơi xuất hiện.
  return street_feature, points, ways