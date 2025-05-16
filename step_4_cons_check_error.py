from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'manager',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='manager-group'
)

for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    print(data['cams'])
    # print(data['results'])