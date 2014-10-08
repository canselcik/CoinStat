#!/usr/bin/python
from AggregateConsumer import AggregateConsumer

host = "amqp://cselcik.com"
exchange = "updates"
routing_type = "direct"
routing_key = ""

consumer = AggregateConsumer(host, exchange)
consumer.start_consuming()
