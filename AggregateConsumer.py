from Subscribe import Subscribe
from Message import *


class AggregateConsumer:
    def __init__(self, host, exchange):
        self.host = host
        self.exchange = exchange

    def start_consuming(self):
        if self.host is None or self.exchange is None:
            return False

        self.s = Subscribe(self.host, self.message_handler, self.exchange)
        self.s.start()

    def get_subscribe_object(self):
        return self.s

    def message_handler(self, message):
        parsed = decode_message(message)
        if parsed is not None:
            print "[%s] (%s) %s" % (parsed.get_time(), parsed.get_type(), parsed.get_body())