from kafka import KafkaConsumer
import json

from manager import Manager

consumer = KafkaConsumer(
    'manager',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='manager-group'
)
manager = Manager()
for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    cams = data['cams']
    results = data['results']
    for i in range(len(cams)):
        manager.run(cams[i], results[i])