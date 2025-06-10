from kafka import KafkaConsumer
from worker.manager import Manager
from worker.process_out_model import Process

import cv2
import json
import base64
import numpy as np

manager = Manager()
processer = Process()

def main(topic = 'check_error', port = 9092):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f'192.168.1.240:{port}',
        auto_offset_reset='latest',
        group_id='video-group',
        value_deserializer=lambda m: m.decode('utf-8')
    )
    print('chay xong topic')
    print(consumer)
    for message in consumer:
        try:
            print('ksdljf_1')
            raw = message.value.decode('utf-8') 
            data = json.loads(raw)
            print('ksdljf')
            if data.get('error', True):
                cam = data['cam']
                print(cam)
                img = base64.b64decode(data['img'])
                img = np.frombuffer(img, np.uint8)
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                cv2.imwrite(f"./infor/img/{cam}.jpg", img)
                result = processer.Add_HSV(data['result'])
                manager.run(img, cam, result, 'All')
        except:
            print('lỗi')
            

if __name__ == '__main__':
    main()