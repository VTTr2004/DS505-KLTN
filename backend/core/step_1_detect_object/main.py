from . import core
import numpy as np

import common
import os

class Step1Detect:
    def __init__(self, model_path):
        self.model = core.Detecter(model_path)

    def detect_and_get_feature(self, imgs):
        # Nhận diện và trích xuất thông tin cần thiết
        objs_list = self.model.transform(imgs)
        for i in range(len(imgs)):
            objs_list[i] = core.extract_3_channel(imgs[i], objs_list[i])
        return objs_list

    def handle(self, cam_names, imgs, current_path=''):
        objs_list = self.detect_and_get_feature(imgs)
        # Cập nhập thông tin mới cho dữ liệu của cam
        data_cams = []
        for name, objs in zip(cam_names, objs_list):
            cam_path = common.get_path_cam(current_path, name)
            temp = core.tracking(cam_path, objs)
            data_cams.append([cam_path, temp])
        return data_cams