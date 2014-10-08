from Subscribe import Subscribe
from Message import *


class AggregateConsumer:
    def __init__(self, host, exchange):
        self.host = host
        self.exchange = exchange
        self.subscribe_object = None

    def start_consuming(self):
        if self.host is None or self.exchange is None:
            return False

        self.subscribe_object = Subscribe(self.host, self.message_handler, self.exchange)
        self.subscribe_object.start()

    def get_subscribe_object(self):
        return self.subscribe_object

    def message_handler(self, message):
        parsed = decode_message(message)
        if parsed is not None:
            print "[%s] (%s) %s" % (parsed.get_field('time'),
                                    parsed.get_field('message_type'),
                                    parsed.get_field('message_content'))
            #parsed.get_field('pos_sent'),
            #parsed.get_field('neg_sent'))
