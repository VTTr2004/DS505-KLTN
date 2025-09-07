from core.visualler import Visualler

class Step2Visual:
    def __init__(self, num_obj, size):
        self.visual = Visualler(num_obj=num_obj, size=size)

    def handle(self, data_cam):
        # Tạo ra dữ liệu cho phần phân loại
        return self.visual.get_img_for_classi(data_cam)