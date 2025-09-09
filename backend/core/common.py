import pickle
import numpy as np
import os

DATA_BLANK = {
    'id_frame':0,
    'objects':[],
    'street_visual':np.zeros((32, 32, 1), dtype=np.uint8)
}

def create_new_path():
    # Tìm một nơi lưu khả dụng
    return ''

def get_path_cam(current_path, cam_name):
    # Lấy địa chỉ lưu dữ liệu của cam
    cam_path = os.path.join(current_path, 'resource', 'data_cams', f"{cam_name}.pkl")
    if not os.path.exists(cam_path):
        os.makedirs(os.path.dirname(cam_path), exist_ok=True)
        with open(cam_path, 'wb') as file:
            pickle.dump(DATA_BLANK, file)
    return cam_path