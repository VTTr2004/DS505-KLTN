import argparse
import cv2
import json
import base64
from kafka import KafkaProducer
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Kafka Producer File Parser")
    parser.add_argument('--file', required=True, help='Path to input file (e.g., video, json)')
    parser.add_argument('--topic', required=False, help='Kafka topic name', default = 'cam')
    parser.add_argument('--port', required=False, default='9092', help='Kafka bootstrap server (default: localhost:9092)')
    return parser.parse_args()

#-------------------------------------------------------------------------------#

def send_file_to_kafka(file_path, topic, port):
    producer = KafkaProducer(bootstrap_servers=f'192.168.1.240:{port}')
    cap = cv2.VideoCapture(file_path)
    cam = file_path.split("\\")[-1].split(".")[0]
    i = 0
    while cap.isOpened():
    
        ret, frame = cap.read()
        if not ret:
            return
        if i <= 15:
            i += 1
            continue
        i = 0
        _, buffer = cv2.imencode('.jpg', frame)
        data = {
            "cam" : cam,
            "img" : base64.b64encode(buffer.tobytes()).decode('utf-8')
        }
        print(data['cam'])
        producer.send(topic, value = json.dumps(data).encode('utf-8'))
        time.sleep(0.5)

    producer.flush()
    cap.release()

if __name__ == '__main__':
    args = parse_args()
    send_file_to_kafka(args.file, args.topic, args.port)