import logging
from queue import Queue
from json import dumps
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="py-producer")
client.connect(host="broker.hivemq.com", port=1883)

def worker(input_queue: Queue):
    while True:
        payload = input_queue.get()
        client.publish(
            topic="sda/test",
            payload=dumps(payload),
        )
        logging.info(f"sending payload over mqttt {dumps(payload)}")

