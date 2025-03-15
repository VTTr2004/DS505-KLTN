import cv2
import numpy as np
import matplotlib.pyplot as plt

class Image_Merger_Labelling:
    def __init__(self, img_lb, img_bg, kind_lb = "Hinh_vuong"):
        # Read image

        self.img_lb = cv2.imread(img_lb)
        self.img_bg = cv2.imread(img_bg)
        self.kind_lb = kind_lb


    #----------------background----------------#
    def Show_bg(self):
        # Show image background

        img = cv2.cvtColor(self.img_bg, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def Size_bg(self):
        # Get height, weight of background

        return self.img_bg.shape[:2]


    #-------------------Label------------------#
    def Show_lb(self):
        # Show image label

        img = cv2.cvtColor(self.img_lb, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.axis("off")
        plt.show()
    
    def Resize_lb(self, fx, fy):
        # Change image

       return cv2.resize(self.img_lb, None, fx = fx, fy = fy)
    
    def Size_lb(self):
        # Get height, weight of label

        return self.img_lb.shape[:2]
    
    def Create_Mask(self, h, w):
        # Delete background for label

        mask = np.zeros((int(h), int(w)), dtype=np.uint8)

        if self.kind_lb == "Hinh_tron":
            r = min(h // 2, w // 2)
            return cv2.circle(mask, (r, r), r, 1, -1)
        
        elif self.kind_lb == 'Hinh_tam_giac':
            points = np.array([[0, h], [w // 2, 0], [w, h]], np.int32)
            return cv2.fillPoly(mask, [points], 1)
        
        # Hinh_vuong
        return np.ones((h, w), dtype=np.float32)     
    

    #------------------Merger------------------#
    def Merge(self, fx, fy, px, py):
        # merge label to background

        img_resize = self.Resize_lb(fx, fy)
        h_lb, w_lb = img_resize.shape[:2]
        mask = self.Create_Mask(h_lb, w_lb)

        temp = self.img_bg.copy()
        roi = temp[py:py + h_lb, px:px + w_lb]
        for c in range(3):
            roi[:, :, c] = (1 - mask) * roi[:, :, c] + mask * img_resize[:, :, c]
        temp[py:py + h_lb, px:px + w_lb] = roi

        return temp
    
    def ShowMerge(self, fx, fy, px, py):
        # show image after merge
 
        temp = self.Merge(fx, fy, px, py)
        temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2RGBA)

        plt.imshow(temp)
        plt.axis("off")
        plt.show()


    #------------------Label------------------#
    def Auto_Labelling(self, fx, fy, px, py, folder_path, name_img, code_lb):
        # Auto merge and save    
        
        h_bg, w_bg = self.Size_bg()
        h_lb, w_lb = self.Size_lb()
        x_max = w_lb * fx + px
        y_max = h_lb * fy + py
        x_min = px
        y_min = py

        x_center = str((x_min + x_max) / (2 * w_bg))
        y_center = str((y_min + y_max) / (2 * h_bg))
        w_box = str((x_max - x_min) / w_bg)
        h_box = str((y_max - y_min) / h_bg)

        with open("./" + folder_path + "/" + name_img + ".txt", 'w') as file:
            file.write(code_lb + " " + x_center + " " + y_center + " " + w_box + " " + h_box)

        return 0