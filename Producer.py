import puka

'''
Usage:
    # All arguments are strings
    p = Producer(host, exchange, routing_type, routing_key)

    # Create a message and send it in string form
    m = Message('status', "HELLO %d" % i)
    p.send(m.str())

    # When done, close connection
    p.disconnect()
'''

class Producer:
    def __init__(self, host, exchange='newsletter', type='fanout', routing_key=''):
        self.host = host
        self.exchange = exchange
        self.type = type
        self.routing_key = routing_key

        self.producer = puka.Client(host)
        self.connect_promise = self.producer.connect()
        self.producer.wait(self.connect_promise)

        self.exchange_promise = self.producer.exchange_declare(exchange=self.exchange, type=self.type)
        self.producer.wait(self.exchange_promise)
        self.running = True

    def disconnect(self):
        self.running = False
        self.producer.close()

    def send(self, m):
        if not self.running or m is None:
            return False
        message_promise = self.producer.basic_publish(exchange=self.exchange,
                                                      routing_key=self.routing_key, body=m)
        self.producer.wait(message_promise)
        return True
