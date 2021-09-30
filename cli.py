import logging
from serial import Serial
from queue import Queue
from threading import Thread

from protocol.datalink.datalink import Datalink

import parser
import producer


serial_input_queue = Queue()
serial_output_queue = Queue()

parser_output_queue = Queue()


input_package =  Queue()

uart = Serial("/dev/tty.usbmodem14223101", 115200, timeout=0.1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logging.info("Program Running")

link = Datalink(
    header=0x7E, uart=uart, input_queue=serial_input_queue, output_queue=serial_output_queue
)

Thread(target=link.run).start()
Thread(target=parser.worker, args=(serial_input_queue, parser_output_queue)).start()
Thread(target=producer.worker, args=(parser_output_queue,)).start()

producer.client.loop_forever()


