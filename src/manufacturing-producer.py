# This script connects to Kafka and send a few messages

from kafka import KafkaProducer
from datetime import datetime, timezone
from uuid import uuid4
from time import sleep
from random import random
import sys
import json

producer = KafkaProducer(
    bootstrap_servers="kakfa-demo-v1-project-2800.aivencloud.com:19995",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

machine_id = str(uuid4()) # Unique ID for each producer

## Allows for Arguments to define the object produced, making it quick to set up multiple producers running in parallel producing different objects

if len(sys.argv) == 1:
    object_produced = 'DefaultObject'
else:
    object_produced = sys.argv[1]

while True: # Run indefinitly, as long as the machine is running
    message_id = str(uuid4()) # Each message has a unique ID
    packet = {
        'timestamp': str(datetime.utcnow().replace(microsecond=0).replace(tzinfo=timezone.utc).isoformat()), # ISO 8601
        'message_id': message_id,
        'machine_id': machine_id,
        'object_produced': object_produced}

    message = json.dumps(packet)
    print(f"Sending Message: {message_id}")
    producer.send("manufacturing", message.encode("utf-8"))

    sleep(random()*5) # Wait up to 5 seconds to add some variety
