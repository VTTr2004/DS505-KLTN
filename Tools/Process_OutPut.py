import numpy as np
import cv2

class ProOP:
    def ExtractHSV(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        H = np.mean(hsv[:, :, 0])
        S = np.mean(hsv[:, :, 1])
        V = np.mean(hsv[:, :, 2])

        return [H, S, V]
    
    def OutForMap(self, img, boxs):
        result = []

        for b in boxs[0].boxes:
            x_1, y_1, x_2, y_2 = map(int, b.xyxy[0])
            HSV = self.ExtractHSV(img[y_1:y_2, x_1:x_2])
            lb = int(b.cls[0])
            result.append([lb, HSV, b.xywh[0].tolist()])

        return result