import numpy as np
import cv2

class ProOP:
    def ExtractHSV(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        H = np.mean(hsv[:, :, 0])
        S = np.mean(hsv[:, :, 1])
        V = np.mean(hsv[:, :, 2])

        return [H, S, V]
    
    def OutForMap(self, img, boxs):
        result = []

        for b in boxs.boxes:
            x_1, y_1, x_2, y_2 = list(map(int, b.xyxy[0]))
            HSV = list(map(float, self.ExtractHSV(img[y_1:y_2, x_1:x_2])))
            lb = int(b.cls[0])
            x_cen = int((x_1 + x_2) / 2)
            y_cen = int((y_1 + y_2) / 2)
            w = int(x_2 - x_1)
            h = int(y_2 - y_1)
            result.append([lb, HSV, [x_cen, y_cen, w, h]])

        return result