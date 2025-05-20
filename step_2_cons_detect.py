from worker.process_out_model import Process

from kafka import KafkaConsumer
from kafka import KafkaProducer

import cv2
import json
import base64
import time
import numpy as np

from ultralytics import YOLO
model = YOLO('./model/final.pt')

def main(topic = 'check_error', port = 9092):

    processer = Process()
    producer = KafkaProducer(bootstrap_servers=f'localhost:{port}')
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f'localhost:{port}',
        auto_offset_reset='latest',
        group_id='video-group'
    )
    for message in consumer:
        raw = message.value.decode('utf-8') 
        data = json.loads(raw)
        imgs = []
        cams = []
        for record in data:
            cam = record['cam']
            img = base64.b64decode(record['img'])
            img = np.frombuffer(img, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            cv2.imwrite(f"./infor/img/{cam}.jpg", img)
            imgs.append(img)
            cams.append(cam)
            
        if not imgs:
            continue
        results = processer.Add_HSV(imgs, model.predict(imgs))
        
        data = {
            'cams': cams,
            'results': results
        }

        producer.send('manager', value = json.dumps(data).encode('utf-8'))
        time.sleep(0.5)


if __name__ == '__main__':
    main()