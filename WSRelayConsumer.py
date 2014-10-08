from Subscribe import Subscribe
from Message import *
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

path = r'/main'
websockets = []


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in websockets:
            websockets.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        if self in websockets:
            websockets.remove(self)


def transmit_all_clients(message):
    print "Transmitting data to %d WS clients" % len(websockets)
    for ws in websockets:
        ws.write_message(message)


class WSRelayConsumer:
    def __init__(self, host, exchange, ws_port, ws_path):
        print "WSRelayConsumer starting"
        self.host = host
        self.exchange = exchange
        self.subscribe_object = None

        # Creating the WS server
        application = tornado.web.Application([(ws_path, WSHandler,)])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(ws_port)
        tornado.ioloop.IOLoop.instance().start()
        print "WSHandler started"

    def start_consuming(self):
        print "Consuming from '%s'" % self.host

        if self.host is None or self.exchange is None:
            return False
        self.subscribe_object = Subscribe(self.host, self.message_handler, self.exchange)
        self.subscribe_object.start()

    def get_subscribe_object(self):
        return self.subscribe_object

    def stop_consuming(self):
        print "Stopping subscription"
        self.subscribe_object.stop()

    def message_handler(self, message):
        parsed = decode_message(message)
        if parsed is not None:
            transmit_all_clients("[%s] (%s) %s" % (parsed.get_field('time'),
                                                   parsed.get_field('message_type'),
                                                   parsed.get_field('message_content')))
