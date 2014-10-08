#!/usr/bin/python
from WSRelayConsumer import *
import signal
import os

# RabbitMQ Settings
host = "amqp://cselcik.com"
exchange = "updates"
routing_type = "direct"
routing_key = ""

# WS Settings
port = 8080
ws_path = r'/main'


def signal_handler(signal, frame):
    print "Exiting..."
    os._exit(0)

consumer = WSRelayConsumer(host, exchange, port, ws_path)
consumer.start_consuming()

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
