import numpy as np
import pickle
from scipy.optimize import linear_sum_assignment

def cal_value_distance(char_old: list, char_new: list):
    result = np.linalg.norm(np.array(char_old)[:, None, :] - np.array(char_new)[None, :, :], axis=2)
    return result

def re_id(objs_old_main: list, objs_new: list) -> list:
    objs_old = np.copy(objs_old_main)
    # Cập nhập ví trí có thể xảy ra từ các vị trí trước
    objs_old[:, 4:6] = objs_old[:, 4:6] + (objs_old[:, 8:10] - objs_old[:, 4:6])*(objs_old[:, -2]+1)
    # Tạo ma trận mẫu
    size_old = len(objs_old)
    size_new = len(objs_new)
    size = max(size_old, size_new)
    matrix = cal_value_distance(objs_old, objs_new)
    matrix_padded = np.full((size, size), fill_value = 1e9)
    matrix_padded[:size_old, :size_new] = matrix
    # Tính chi phí tối ưu nhất
    old_ind, new_ind = linear_sum_assignment(matrix_padded)
    result = [[], []]
    temp = []
    # Lọc chi phí tối ưu
    for i, j in zip(old_ind, new_ind):
        if i < size_old and j < size_new:
            temp.append(cal_value_distance([objs_old[i]], [objs_new[j]]))
    Q1 = np.percentile(temp, 25)
    Q3 = np.percentile(temp, 75)
    val_max = Q3 + 1.5*(Q3 - Q1)
    if val_max > 5000:
        return [], []
    # val_max = 100
    for i, j in zip(old_ind, new_ind):
        if i < size_old and j < size_new and cal_value_distance([objs_old[i]], [objs_new[j]]) < val_max:
            result[0].append(i)
            result[1].append(j)
    return result[0], result[1]

def update_infor(objs_old: list, objs_new: list) -> None:
    if len(objs_old) == 0:
        return objs_new
    if len(objs_new) == 0:
        objs_old[:, -2] += 1
        return objs_old
    objs_old = np.array(objs_old)
    objs_new = np.array(objs_new)
    old_id, new_id = re_id(objs_old[:, :6], objs_new[:, :6])
    # Cập nhập giá trị mới
    objs_old[old_id, 10:14] = objs_old[old_id, 8:12]
    objs_old[old_id, 8: 10] = objs_old[old_id, 4:6]
    objs_old[old_id, :8] = objs_new[new_id, :8]
    # Loại bỏ obj ra khỏi vùng quan sát và cập nhập chỉ số theo dõi
    objs_old[[i not in old_id for i in range(len(objs_old))], -2] += 1
    objs_old[[i in old_id for i in range(len(objs_old))], -2] = 0
    objs_old = objs_old[objs_old[:, -2] < 15]
    # Thêm obj mới
    objs_new = objs_new[[i not in new_id for i in range(len(objs_new))]]
    if len(objs_new) != 0:
        objs_old = np.vstack((objs_old, objs_new))
    return objs_old.tolist()

def tracking(cam_path, objs_new):
    with open(cam_path, 'rb') as file:
        data_cam = pickle.load(file)

    data_cam['id_frame'] += 1
    data_cam['objects'] = update_infor(data_cam['objects'], objs_new)
    xs = [obj[4] for obj in objs_new]
    ys = [obj[5] for obj in objs_new]
    data_cam['street_visual'][np.array(xs), np.array(ys)] = 50

    return data_cam