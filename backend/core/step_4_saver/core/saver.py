import pickle
import numpy as np

class Saver:
    def __init__(self):
        self.version = 1.0

    @staticmethod
    def save(obj, id_frame):
        pass
    
    def check_new_vio_traffic(self, data_cam, preds):
        preds = np.array(preds).reshape(-1, 1)
        objs = np.array(data_cam['objects'])
        # Trường hợp lỗi mới
        mask = (preds==1) & (objs[:,1]==0)
        for obj in objs[mask]:
            self.save(obj, data_cam['id_frame'])
        # Bật cờ báo lỗi lên
        objs[mask,-1] = preds[mask]
        data_cam['objects'] = list(objs)
        return data_cam