import puka
from threading import Thread


class Subscribe:
    def __init__(self, host, on_message, exchange='newsletter'):
        self.host = host
        self.exchange = exchange
        self.on_message = on_message
        self.running = True

    def stop(self):
        self.running = False

    def _consume(self):
        # declare and connect a consumer
        consumer = puka.Client(self.host)
        connect_promise = consumer.connect()
        consumer.wait(connect_promise)

        # create temporary queue
        queue_promise = consumer.queue_declare(exclusive=False)
        queue = consumer.wait(queue_promise)['queue']

        # bind the queue to newsletter exchange
        bind_promise = consumer.queue_bind(exchange=self.exchange, queue=queue)
        consumer.wait(bind_promise)

        # start waiting for messages on the queue created beforehand and print them out
        message_promise = consumer.basic_consume(queue=queue, no_ack=True)

        while self.running:
            message = consumer.wait(message_promise)
            self.on_message(message['body'])
        consumer.close()

    def start(self):
        self.running = True
        try:
            thread = Thread(target=self._consume)
            thread.start()
            return True
        except:
            print "An error occurred when creating a Thread for getting messages"
        return False
