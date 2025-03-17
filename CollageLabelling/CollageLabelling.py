import cv2
import random
import numpy as np
import matplotlib.pyplot as plt

#---------------label---------------#
class Label_Img:
    def __init__(self, img_path, kind_lb):
        self.img_lb = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        self.kind_lb = kind_lb

    def Show(self):
        # 

        plt.imshow(self.img_lb)
        plt.axis("off")
        plt.show()

    def Resize_lb(self, ratio):
        #

        return cv2.resize(self.img_lb, None, fx = ratio, fy = ratio)
    
    def Size_lb(self):
        # return height, weight of label

        return self.img_lb.shape[:2]
    
    def Create_Mask(self, h, w):
        # Use for delete background of label

        mask = np.zeros((int(h), int(w)), dtype = np.int32)

        if self.kind_lb == "tron":
            r = min(h // 2, w // 2)
            return cv2.circle(mask, (r, r), r, 1, -1)
        
        elif self.kind_lb == "tam_giac":
            points = np.array([[0, h], [w // 2, 0], [w, h]], np.int32)
            return cv2.fillPoly(mask, [points], 1)
        
        #Hinh_vuong
        return np.ones((h, w), dtype = np.int32)
    
    
#-------------------background---------------------#
class Background_Img:
    def __init__(self,img_path):
        self.bg_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

    def Show(self):
        #

        plt.imshow(self.bg_img)
        plt.axis("off")
        plt.show()
    
    def Size_bg(self):
        # Return size of background

        return self.bg_img.shape[:2]
    
    def Get_Matric(self):
        #

        return self.bg_img

#---------------------------merge---------------------------#
class Image_Merger_Labelling:
    def __init__(self, lb_list, bg):
        self.lb_list = lb_list
        self.address = []
        for lb in self.lb_list:
            self.address.append([0,0])
        self.bg = bg
        

    def Cal_Size_Lb(self, lb, ratio):
        # change size of label for label take <ratio>% of background

        h_bg, w_bg = self.bg.Size_bg()
        h_lb, w_lb = lb.Size_lb()
        
        return (h_bg * w_bg * ratio) / (h_lb * w_lb)


    def Merge(self):
        # merge label to background

        result = self.bg.Get_Matric().copy()

        for i in range(len(self.lb_list)):
            try:
                lb = self.lb_list[i]
                ratio = random.uniform(0.5, 0.6)
                img_resize = lb.Resize_lb(ratio)
                h_lb, w_lb = img_resize.shape[:2]
                mask = lb.Create_Mask(h_lb, w_lb)
                px = int((random.random() * 500) % 500)
                py = px
                self.address[i] = [px, py, ratio]
    
                roi = result[py:py + h_lb, px:px + w_lb]
                for c in range(3):
                    roi[:, :, c] = (1 - mask) * roi[:, :, c] + mask * img_resize[:, :, c]
                result[py:py + h_lb, px:px + w_lb] = roi
            except:
                lb.Show()

        return result
    
    def ShowMerge(self):
        # show image after merge
 
        temp = self.Merge()
        # temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2RGBA)

        plt.imshow(temp)
        plt.axis("off")
        plt.show()


    #------------------Label------------------#
    def Auto_Labelling(self, folder_path, name_img, code_lb):
        # Auto merge and save    
        
        temp = []
        for i in range(len(self.lb_list)):
            lb = self.lb_list[i]
            h_bg, w_bg = self.bg.Size_bg()
            h_lb, w_lb = lb.Size_lb()
            px = self.address[i][0]
            py = self.address[i][1]
            ratio = self.address[i][2]

            x_max = w_lb * ratio + px
            y_max = h_lb * ratio + py
            x_min = px
            y_min = py

            x_center = str((x_min + x_max) / (2 * w_bg))
            y_center = str((y_min + y_max) / (2 * h_bg))
            w_box = str((x_max - x_min) / w_bg)
            h_box = str((y_max - y_min) / h_bg)

            temp.append(code_lb + " " + x_center + " " + y_center + " " + w_box + " " + h_box)

        with open("./" + folder_path + "/" + name_img + ".txt", 'w') as file:
            for t in temp:
                file.write(t + "\n")

        return 0
    