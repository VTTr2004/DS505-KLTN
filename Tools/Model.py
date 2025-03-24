from ultralytics import YOLO

class Model:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def Predict(self, img_ip):
        # Detect object

        ip_deepsort = [] # [x, y, w, h, confidence, class_id]

        results = self.model.predict(img_ip, save = False)
        for result in results:  
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                
                ip_deepsort.append([x1, y1, x2 - x1, y2 - y1, conf, cls_id])

        return ip_deepsort