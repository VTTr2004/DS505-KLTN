import pickle
import numpy as np

DATA_BLANK = {
    'id_frame':0,
    'objects':[],
    'street_visual':np.zeros((32, 32, 1), dtype=np.uint8)
}

def create_new_path():
    # Tìm một nơi lưu khả dụng
    return ''

def get_path_cam(cam_name):
    # Lấy địa chỉ lưu dữ liệu của cam
    try:
        return ''
    except:
        new_path = create_new_path()
        with open(new_path, 'wb') as file:
            pickle.dump(DATA_BLANK, file)
        return new_path