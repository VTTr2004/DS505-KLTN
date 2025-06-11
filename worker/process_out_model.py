import numpy as np
import cv2

class Process:

    @staticmethod
    def Extract_HSV(img, box):
        h_img, w_img = img.shape[:2]
        x_min = max(0, int(box[0] - box[2] / 2))
        y_min = max(0, int(box[1] - box[3] / 2))
        x_max = min(w_img, int(box[0] + box[2] / 2))
        y_max = min(h_img, int(box[1] + box[3] / 2))
        h = np.mean(img[y_min:y_max, x_min:x_max, 0]) / 255. * 100
        s = np.mean(img[y_min:y_max, x_min:x_max, 1]) / 255. * 100
        v = np.mean(img[y_min:y_max, x_min:x_max, 2]) / 255. * 100
        return [h, s, v]
    
    @staticmethod
    def Add_HSV_2(img, results):
        cls_id = [r[0] for r in results]
        boxes = [r[1:] for r in results]
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        temp = [
            list(map(float, [cls*100000] + list(map(float, Process.Extract_HSV(img_hsv, box))) + list(map(float, box)))) 
            for cls, box in zip(cls_id, boxes)
        ]

        return temp

    @staticmethod
    def Add_HSV(img, cls_list, box_list) -> list:
        pro_results = []
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        temp = [
            list(map(float, [cls*100000] + list(map(float, Process.Extract_HSV(img_hsv, box))) + list(map(float, box)))) 
            for cls, box in zip(cls_list, box_list)
        ]
        pro_results.append(temp)

        return pro_results