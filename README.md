# aiven-kafka-demo
Interview Assignment

## Setting Up Kakfa in Aiven

### Creating the service

Once you've got an account, and have successfully logged in to the Aiven Console, just click "+ Create a new service" in the top right.

1. Service - We'll set up Kafka first, so choose that, and leave the default version.
2. Provider - Choose whichever cloud provider you like best, or whichever gives you the best deal, doesn't matter to us, they will all work together seamlessly.
3. Region - Generally you'll want something close to your office, home, or datacenter to reduce latency, but anywhere will work for this demo.
4. Service Plan - Choose the cheapest one, which will almost certainly be under the "Startup" tab. These plans are ideal for demos and testing.
5. Name - Choose a descriptive name, but don't sweat it, we'll only need one service for this demo, so it should be easy to keep track of.

The service will take a few minutes to provision, but you can start checking it out by just clicking on the service name. You'll want to download the Access Key, the Access Certificate, and the CA Certificate to you machine. These will allow you to authenticate to the service and actually write to a Kafka topic. While you are here, also enable Kafka REST API (Karapace), which will allow you to check the what's been written to your topic, right in the Aiven Console.

![Download Keys and Certs](/images/Certs.jpg)

Once your service is Running, click over to the "Topics" tab and create a new topic. The demo code provided in this repository uses a topic named "manufacturing". Once created, it will appear in the Topic List below, from there you can check the setting and status of the topic and any consumers it has.

Now we'll need to create a producer to write to this topic.

## A Quick Python Kafka producer

If you don't already have it, you'll need to install Kafka-Python:

'''pip install kafka-python'''

Next you'll need to create your producer.

'''
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka-1d98b26-project-2800.aivencloud.com:19995", # Service URI
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)
'''

The service URI can be found on the "Overview" tab of the service page. You'll also need to put the three files you downloaded earlier in the folder with the python script, ca.pem, service.cert, and service.key.

***IF YOU ARE CHECKING THIS PYTHON CODE INTO A PUBLIC GIT REPO DO NOT CHECK THESE FILES IN, IT WOULD ALLOW ANYONE TO ACCESS YOUR SERVICES***

Next you just need to write some stuff to your topic using this Producer. "manufacturing" here is the topic, so if you named yours something different, don't forget to change it.

'''
message = 'Dear Kafka'
print("Sending Message")
producer.send("manufacturing", message.encode("utf-8"))
'''

## Making Sure it's Working
Before we go further, we want to make sure our Producer is working, and there are two good ways to do so.

### In the Aiven Console

In the "Topics" tab on the Service, you can find your topic in the "Topics List" section, and click on it to bring up the Info page. Among other useful things on this page, in the top right corner, you'll find the "Messages" button, which brings up the Messages screen for this topic. Here you can use "Fetch Messages" to see what is in the queue. The only downside is, they need to be formatted in JSON or Avro to be readable (unless you can read binary), and the message in the sample code above was plain text. To remedy this you can either check out the sample code, which encodes a packet of useful information as JSON and writes it to the topic, or you can consume it ...

### With a Python Consumer

Python consumers are quite simple, but have a few more configuration elements:
'''
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
'''

Then you can just create a simple loop to check regularly for newly published updates to your topic like so:

'''
while True: #Listen for messages indefinitly
    raw_msgs = consumer.poll(timeout_ms=100)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print(f"Received: {msg.value}")
    consumer.commit()
'''

## Checking the Logs and Making some Charts


Add to/Update git ignore for certs/keys/pem

Need to enable Kafka REST API to see messages in queues
