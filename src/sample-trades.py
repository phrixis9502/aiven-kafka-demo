# This script connects to Kafka and send a few messages

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kakfa-demo-v1-project-2800.aivencloud.com:19995",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

for i in range(1, 4):
    message = "message number {}".format(i)
    print("Sending: {}".format(message))
    producer.send("demo-topic", message.encode("utf-8"))

# Force sending of all messages

producer.flush()
