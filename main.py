#!/usr/bin/python
from AggregateConsumer import AggregateConsumer
from Producer import Producer
from Message import Message
import time

host = "amqp://cselcik.com"
exchange = "updates"
routing_type = "direct"
routing_key = ""

consumer = AggregateConsumer(host, exchange)
consumer.start_consuming()

p = Producer(host, exchange, routing_type, routing_key)
for i in range(10):
    m = Message('status', "HELLO %d" % i)
    p.send(m.str())
    time.sleep(0.1)
