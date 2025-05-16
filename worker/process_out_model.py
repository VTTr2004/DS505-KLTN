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
        h = np.mean(img[x_min:x_max, y_min:y_max, 0])
        s = np.mean(img[x_min:x_max, y_min:y_max, 1])
        v = np.mean(img[x_min:x_max, y_min:y_max, 2])
        return [h, s, v]
    
    def Add_HSV(self, imgs, results) -> list:
        pro_results = []
        
        for i in range(len(imgs)):
            cls_id = results[i].boxes.cls.cpu().numpy()
            boxes = results[i].boxes.xywh.cpu().numpy()
            img_hsv = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2HSV)
            temp = [
                list(map(float, [cls] + list(map(float, self.Extract_HSV(img_hsv, box))) + list(map(float, box)))) 
                for cls, box in zip(cls_id, boxes)
            ]
            pro_results.append(temp)

        return pro_results