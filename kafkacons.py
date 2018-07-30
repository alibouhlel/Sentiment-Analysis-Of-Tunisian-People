from kafka import KafkaConsumer

KAFKA_TOPIC = 'demo'

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest')
for message in consumer:
    print(message.value)

