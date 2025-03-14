import cv2
import matplotlib.pyplot as plt

class Image_Merger:
    def __init__(self, img_lb, img_bg):
        # Read image

        self.img_lb = cv2.imread(img_lb)
        self.img_bg = cv2.imread(img_bg)

    def Show_lb(self):
        # Show image label

        img = cv2.cvtColor(self.img_lb, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def Show_bg(self):
        # Show image background

        img = cv2.cvtColor(self.img_bg, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def Resize_lb(self, fx, fy):
        # Change image

       return cv2.resize(self.img_lb, None, fx = fx, fy = fy)
    
    def Size_lb(self):

        return self.img_lb.shape

    def Merge(self, fx, fy, px, py):
        # merge label to background

        img_resize = self.Resize_lb(fx, fy)
        h, w, _ = img_resize.shape
        temp = self.img_bg
        temp[py:py + h, px:px + w] = img_resize

        return temp

    def ShowMerge(self, fx, fy, px, py):
 
        temp = self.Merge(fx, fy, px, py)
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)

        plt.imshow(temp)
        plt.axis("off")
        plt.show()