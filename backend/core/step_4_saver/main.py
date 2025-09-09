from .core.saver import Saver

class Step4Save:
    def __init__(self):
        self.saver = Saver()

    def handle(self, data_cam, preds):
        return self.saver.check_new_vio_traffic(data_cam, preds)