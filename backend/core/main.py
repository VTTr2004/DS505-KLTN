from step_1_detect_object.main import Step1Detect
from step_2_transform_visual.main import Step2Visual
from step_3_classify_violation.main import Step3Classi
from step_4_saver.main import Step4Save

import pickle

class CONFIG:
    size = 32
    num_obj = 5
    model_detection_path = 'resource/models/pt1.pt'
    model_classify_path = 'resource/models/pt2.pth'

STEP_1 = Step1Detect(CONFIG.model_detection_path)
STEP_2 = Step2Visual(CONFIG.num_obj, CONFIG.size)
STEP_3 = Step3Classi(CONFIG.model_classify_path)
STEP_4 = Step4Save()

def auto_handle(cam_names, imgs):
    # Nhận diện vật thể và rắn lại id
    data_cams = STEP_1.handle(cam_names, imgs)
    # Phân loại lỗi
    for cam_path, data_cam in data_cams:
        imgs = STEP_2.handle(data_cam)
        preds = STEP_3.handle(imgs)
        data_cam = STEP_4.handle(data_cam, preds)
        with open(cam_path, 'wb') as file:
            data_cam = pickle.dump(data_cam, file)