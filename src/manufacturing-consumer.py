from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "manufacturing", #Topic Name
    auto_offset_reset="earliest",
    bootstrap_servers="kakfa-demo-v1-project-2800.aivencloud.com:19995", # Service URI
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

while True: #Listen for messages indefinitly
    raw_msgs = consumer.poll(timeout_ms=100)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print(f"Received: {msg.value}")
    consumer.commit()
