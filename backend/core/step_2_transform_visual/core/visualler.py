import numpy as np
import pickle
import random

class Visualler:
    def __init__(self, num_obj, size):
        self.num_obj=num_obj
        self.size=size
    
    def read_cam(self, cam_path):
        with open(cam_path, 'rb') as file:
            data = pickle.load(file)
        self.visual = data['street_visual']
        self.objs = data['objects']

    @staticmethod
    def change_point(val_now, val_before):
        if val_before == 0:
            return 0
        if val_before < val_now:
            return -1
        if val_before > val_now:
            return 1
        return 0

    def get_img_for_classi(self, data_cam):
        result_final = []
        for obj in data_cam['objects']:
            result = np.copy(data_cam['street_visual'])
            # Lấy số lượng obj cần thiết
            obj_temps = data_cam['objects']
            if len(data_cam['objects']) > self.num_obj:
                obj_temps = random.sample(data_cam['objects'], self.num_obj)
            # Vẽ các obj phụ
            for o_t in obj_temps:
                x1 = o_t[4]
                x2 = o_t[8] 
                x2 += self.change_point(x1, x2)
                x2 = min(self.size, max(0, x2))
                y1 = o_t[5]
                y2 = o_t[9]
                y2 += self.change_point(y1, y2)
                y2 = min(self.size, max(0, y2))
                if x1 + 2 <= self.size and y1 + 2 <= self.size:
                    result[x1:x1+2, y1:y1+2] = 150
                if x2 + 2 <= self.size and y2 + 2 <= self.size and x2 != 0 and y2 != 0:
                    result[x2:x2+2, y2:y2+2] = 100
                result_final.append(result)
            # Vẽ obj chính
            result = np.copy(data_cam['street_visual'])
            x1 = obj[4]
            x2 = obj[8] 
            x2 += self.change_point(x1, x2)
            x2 = min(self.size, max(0, x2))
            y1 = obj[5]
            y2 = obj[9]
            y2 += self.change_point(y1, y2)
            y2 = min(self.size, max(0, y2))
            if x1 + 2 <= self.size and y1 + 2 <= self.size:
                result[x1:x1+2, y1:y1+2] = 150
            if x2 + 2 <= self.size and y2 + 2 <= self.size and x2 != 0 and y2 != 0:
                result[x2:x2+2, y2:y2+2] = 100
            result_final.append(result)
        return np.array(result_final).astype(np.uint8)