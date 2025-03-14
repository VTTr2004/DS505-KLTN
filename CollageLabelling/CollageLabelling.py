import cv2

class Image_Merger:
    def __init__(self, img_lb, img_bg):
        # Read image

        self.img_lb = cv2.imread(img_lb)
        self.img_bg = cv2.imread(img_bg)

    def Show_lb(self):
        # Show image label

        cv2.imshow("Label",self.img_lb)

    def Show_bg(self):
        # Show image label

        cv2.imshow("Background",elf.img_bg)

print(cv2.__file__)