import random
import numpy as np

# Hằng Số.
PARAM_CHAR = {
    'x':0,
    'y':0,
    'd_x':0,
    'd_y':0,
    'last':0,
    'trend':0,
}
NEW = np.array(list(PARAM_CHAR.values()))

def get_gate(ways):
  # Xác định các điểm nào là nơi Vật Thể xuất hiện.
  result = [key for key, item in ways.items() if item['gate_in'] == 1]
  return result

def get_new_trend(chars:np.ndarray, code_pixels, ways, code_situation, have_false = True):
  # Xử lý các Vật Thể khi gặp các góc rẽ
  for i in range(len(chars)):
    situation = ways[code_pixels[i]-2].get('code_situation', -1)
    # Nếu thỏa điều của của toàn map (Mô phỏng đèn đỏ).
    if situation != -1 and situation != code_situation:
      continue
    # Đổi một Vật Thể thành phạm lỗi (Trong mọi tình huống đều có nhiều nhất 1 Vật Thể đi sai).
    if not have_false:
      if chars[i,-1] == 0:
        chars[i,-1] = np.random.choice([1,0], p=[0.1, 0.9])
        if chars[i, -1] == 1:
          have_false = True
    def get_status(status):
      # Xác định trạng thái của Vật Thể.
      if status == 0:
        return 'true_trend'
      return 'false_trend'
    # Lấy hướng đi mới của Vật Thể.
    status = get_status(chars[i,-1])
    trends = ways[code_pixels[i]-2][status]
    if len(trends) == 0:
      chars[i, -1] = 2
      continue
    trend = random.choice(trends)
    # Cập nhập dữ liệu mới.
    chars[i,2:5] = np.array(trend)
    # Đổi vị trí theo hướng mới.
    chars[i,0] += chars[i,2]
    chars[i,1] += chars[i,3]
  return chars

def create_char(chars, gates, points, ways):
    # Tạo thêm Vật Thể Mới
    gate = np.random.choice(gates)
    new_char = NEW.copy()
    x1,y1,x2,y2 = list(points[points[:, 0]==gate, 1:])[0]
    def safe_randint(a, b):
        # Tạo ngẫu nhiên vị trí.
        if a == b:
            return a
        return np.random.randint(min(a, b), max(a, b)) if a != b else a
    new_char[0]=safe_randint(x1, x2)
    new_char[1]=safe_randint(y1, y2)
    new_char = get_new_trend(np.array([new_char]), [gate+2], ways, ways[gate+2]['code_situation'])[0]
    if len(chars) == 0:
        return np.array([new_char])
    chars = np.vstack([chars, new_char])
    return chars

def get_pixel(street_feature, x, y):
    try:
        return street_feature[x, y]
    except:
        return 0

def update_char(chars:np.ndarray, street_feature, ways, code_situation=0):
    # Cập nhập thông số của vật thể liên tục.
    if len(chars) == 0:
        return chars
    have_false = True if 1 in chars[:, -1] else False
    xs = chars[:,0] + chars[:,2]
    ys = chars[:,1] + chars[:,3]
    # Lấy giá trị pixel tại vị trí (xs, ys).
    code_pixels = np.array([get_pixel(street_feature, x, y) for x, y in zip(xs, ys)])
    # 1. Gặp đường: đi bình thường.
    mask1 = (code_pixels == 1) | (chars[:,-1] == 1)
    chars[mask1, 0] = xs[mask1]
    chars[mask1, 1] = ys[mask1]
    # 2. Gặp gặp góc rẽ.
    mask2 = (code_pixels > 1) & (~mask1)
    if np.any(mask2):
        chars[mask2] = get_new_trend(chars[mask2], code_pixels[mask2], ways,code_situation, have_false)
    # 3. Loại bỏ các Vật Thể ra khỏi tầm quan sát.
    mask3 = (code_pixels > 0) & (chars[:, -1] < 2)
    chars = chars[mask3,:]
    return chars