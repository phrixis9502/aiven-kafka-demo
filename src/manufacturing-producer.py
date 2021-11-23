# This script connects to Kafka and send a few messages

from kafka import KafkaProducer
import json
import datetime
import uuid
import sys
import time
import random

producer = KafkaProducer(
    bootstrap_servers="kakfa-demo-v1-project-2800.aivencloud.com:19995",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

machine_id = str(uuid.uuid4())

if len(sys.argv) == 1:
    object_produced = 'Default Object'
else:
    object_produced = sys.argv[1]

print(machine_id)
print(object_produced)

while True:
    message_id = str(uuid.uuid4())
    packet = {
        'timestamp': str(datetime.datetime.utcnow().replace(microsecond=0).replace(tzinfo=datetime.timezone.utc).isoformat()),
        'message_id': message_id,
        'machine_id': machine_id,
        'object_produced': object_produced}

    message = json.dumps(packet)
    print(f"Sending Message: {message_id}")
    producer.send("manufacturing", message.encode("utf-8"))

    time.sleep(random.random()*5)
    # Force sending of all messages
producer.flush()
