from manager import Manager

from kafka import KafkaConsumer

import cv2
import argparse
import json
import pickle
import numpy as np

# def parse_args():
#     parser = argparse.ArgumentParser(description="Kafka Consumer File Parser")
#     parser.add_argument('--port', required=True, help='Kafka bootstrap server port (e.g., 9092)')
#     parser.add_argument('--topic', required=True, help='Kafka topic name')
#     return parser.parse_args()

#-------------------------------------------------------------------------------#

def main(topic = 'chars', port = 9092):

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f'localhost:{port}',
        auto_offset_reset='earliest',
        group_id='video-group'
    )

    manager = Manager()

    for message in consumer:
        data = pickle.loads(message.value.decode('utf-8'))
        for d in data:
            cam = d[0]['cam']
            img = d[0]['data']
            chars = d[1]
            # manager.run(cam, chars)
            print(cam)



if __name__ == '__main__':
    # arg = parse_args()
    # main(arg.topic, arg.port)
    main()