import logging
from serial import Serial
from queue import Queue
from threading import Thread
from json import loads

from protocol.datalink.datalink import Datalink

import parser2
import producer


serial_input_queue = Queue()
serial_output_queue = Queue()

parser_output_queue = Queue()


input_package =  Queue()

uart = Serial("COM3", 115200, timeout=0.1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logging.info("Program Running")

link = Datalink(
    header=0x7E, uart=uart, input_queue=serial_input_queue, output_queue=serial_output_queue
)

Thread(target=link.run).start()
Thread(target=parser2.worker, args=(serial_input_queue, parser_output_queue)).start()
Thread(target=producer.worker, args=(parser_output_queue,)).start()

def on_message(client, userdata, msg):
    print("me llego")
    if msg.topic=="sda/arduino":
        keys={
            "led":0x0A,
            "rgb":0x00
        }
        colores = {
            "rojo":bytearray.fromhex("FF0000"),
            "verde":bytearray.fromhex("00FF00"),
            "azul":bytearray.fromhex("0000FF"),
            "rosado":bytearray.fromhex("7a2055"),
            "cielo":bytearray.fromhex("1d6e66"),
            "blanco":bytearray.fromhex("545454"),
            "apagado":bytearray.fromhex("000000")
        }
        if msg.payload == b"pot":
            print("aca")
            pack = bytearray.fromhex("7E0101FE") # Conseguir dato del potenciometro
            uart.write(pack)
        else:
            try:
                data=loads(msg.payload)
            except:
                return
            for k in data:
                payload = bytearray()
                payload.append(0x7E) # Header
                payload.append(0x04) # SIze
                key = keys.get(k,-1)
                if key ==-1: # Verificar key
                    break
                pack = bytearray()
                pack.append(key)
                
                # Calculo pack
                if k == "led" and data[k]==1:
                    pack.extend(bytearray.fromhex("010000"))
                elif k == "led" and data[k]==0:
                    pack.extend(bytearray.fromhex("000000"))
                elif k == "rgb":
                    color = colores.get(data[k],-1)
                    if color==-1:
                        break
                    pack.extend(color)
                checksum = 0xFF - sum(pack)
                payload.extend(pack)
                payload.append(checksum)
                uart.write(payload)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sda/arduino")
def on_disconnect(client, userdata, flags, rc):
    print("Me desconecte")
def on_subscribe(client, userdata, flags, rc):
    print("me subscribi")

producer.client.on_message = on_message
producer.client.on_connect = on_connect
producer.client.on_disconnect = on_disconnect
producer.client.on_subscribe = on_subscribe
producer.client.connect(host="broker.emqx.io", port=1883)
producer.client.loop_forever()

