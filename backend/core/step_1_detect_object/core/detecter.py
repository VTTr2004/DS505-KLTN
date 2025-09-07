from ultralytics import YOLO

class Detecter:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def transform(self, imgs):
        return self.model.predict(imgs)