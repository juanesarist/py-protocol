import logging
from time import sleep
from queue import Queue
from protocol.package.package import Package


def worker(input_queue: Queue, ouput_queue: Queue):
    while True:
        payload = input_queue.get()
        pack = Package(payload=payload)
        logging.info(f"Package added to Queue {pack.dict()}")
        ouput_queue.put(pack.dict())
