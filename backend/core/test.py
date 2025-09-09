from step_1_detect_object.main import Step1Detect
# from step_2_transform_visual.main import Step2Visual
# from step_3_classify_violation.main import Step3Classi
# from step_4_saver.main import Step4Save

from main import CONFIG

# Hằng Số
STEP_1 = Step1Detect(CONFIG.model_detection_path)
# STEP_2 = Step2Visual(CONFIG.num_obj, CONFIG.size)
# STEP_3 = Step3Classi(CONFIG.model_classify_path)
# STEP_4 = Step4Save()

import cv2
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_step1(img_path):
    cap = cv2.imread(img_path, cv2.IMREAD_COLOR_RGB)
    resutls = STEP_1.handle(['cam_test'],[cap], CURRENT_DIR)
    print(resutls)

test_step1(os.path.join(CURRENT_DIR, 'resource', 'data_test', 'img_test.png'))