from core.classi_er import ClassiEr

class Step3Classi:
    def __init__(self, model_path):
        self.model = ClassiEr(model_path)

    def handle(self, imgs):
        return self.model.classify(imgs)