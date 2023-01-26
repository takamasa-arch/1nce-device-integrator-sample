import time as t
import osiot_info
import signal
import sys
import logging
from datetime import datetime
import grovepi
import traceback
import socket
import struct

ENDPOINT = osiot_info.ENDPOINT
CLIENT_ID = osiot_info.CLIENT_ID
PORT = osiot_info.PORT

wait_time = 300
device_name = CLIENT_ID

serv_address = (ENDPOINT, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.basicConfig()

def device_main():

    logger.info("Connecting to %s with client ID '%s' to UDP endpoints ...", ENDPOINT, CLIENT_ID)

    while True:

        temp, humi = grovepi.dht(6, 0)
        payload = bytearray(struct.pack('f',temp)) + bytearray(struct.pack('f',humi))
        logger.info(
            "Sending UDP message to {}:{} with body {}".format(
            ENDPOINT,
            PORT,
            payload))

        send_len = sock.sendto(payload, serv_address)

        t.sleep(wait_time)

def exit_sample(msg_or_exception):

    if isinstance(msg_or_exception, Exception):
        logger.error("Exiting sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    else:
        logger.info("Exiting: %s", msg_or_exception)

    logger.info("Disconnecting...")
    sys.exit(0)

def exit_handler(_signal, frame):

    exit_sample(" Key abort")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)

    device_main()