# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import osiot_info
import signal
import sys
import logging
from datetime import datetime
import grovepi
import traceback
import socket

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = osiot_info.ENDPOINT
CLIENT_ID = osiot_info.CLIENT_ID

wait_time = 300
device_name = CLIENT_ID

M_SIZE = 1024

# Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
serv_address = (ENDPOINT, 4445)

# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.basicConfig()

def device_main():

    logger.info("Connecting to %s with client ID '%s' to UDP endpoints ...", ENDPOINT, CLIENT_ID)

    while True:
        # now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        temp, humi = grovepi.dht(6, 0)

        payload = "TEMP:" + str(temp) + ", HUMI:" + str(humi)
        logger.debug("  payload: %s", payload)

        send_len = sock.sendto(payload.encode('utf-8'), serv_address)
        # ※sendtoメソッドはkeyword arguments(address=serv_addressのような形式)を受け付けないので注意

        t.sleep(wait_time)

def exit_sample(msg_or_exception):
    """
    Exit sample with cleaning

    Parameters
    ----------
    msg_or_exception: str or Exception
    """
    if isinstance(msg_or_exception, Exception):
        logger.error("Exiting sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    else:
        logger.info("Exiting: %s", msg_or_exception)

    logger.info("Disconnecting...")
    sys.exit(0)

def exit_handler(_signal, frame):
    """
    Exit sample
    """
    exit_sample(" Key abort")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)

    device_main()