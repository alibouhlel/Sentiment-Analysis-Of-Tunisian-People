from kafka import KafkaProducer

KAFKA_TOPIC = 'demo'

producer = KafkaProducer(bootstrap_servers='localhost:9092')
# Must send bytes
messages = [b'hello kafka', b'I am sending', b'3 test messages']

# Send the messages
for m in messages:
    producer.send(KAFKA_TOPIC, m)
print "pl"