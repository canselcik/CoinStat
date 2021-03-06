from Subscribe import Subscribe
from Message import *
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from threading import Thread
import tornado.web

path = r'/main'
websockets = []
buffered_history = []


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "A websocket client connected"
        if self not in websockets:
            websockets.append(self)
            self.send_buffered_history()

    def send_buffered_history(self):
        for pair in buffered_history:
            self.write_message("[%s] (%s) %s" % (pair[0], "twitter-buffer", pair[1]))

    def on_message(self, message):
        pass

    def on_close(self):
        if self in websockets:
            websockets.remove(self)


def transmit_all_clients(message):
    print "Transmitting data to %d WS clients" % len(websockets)
    for ws in websockets:
        ws.write_message(message)


def append_to_buffered_history(pair):
    if len(buffered_history) == 24 * 60 / 5 - 1:
        buffered_history = buffered_history[1:]
    buffered_history.append(pair)


class WSRelayConsumer:
    def __init__(self, host, exchange, ws_port, ws_path):
        print "WSRelayConsumer starting"
        self.host = host
        self.exchange = exchange
        self.subscribe_object = None
        self.ws_port = ws_port
        self.ws_path = ws_path

    def start_consuming(self):
        print "Consuming from '%s'" % self.host

        if self.host is None or self.exchange is None:
            return False

        ws_thread = Thread(target=self._ws_listen)
        ws_thread.start()

        self.subscribe_object = Subscribe(self.host, self.message_handler, self.exchange)
        self.subscribe_object.start()

    def _ws_listen(self):
        # Creating the WS server
        application = tornado.web.Application([(self.ws_path, WSHandler)])
        http_server = tornado.httpserver.HTTPServer(application)
        print "WSHandler started"
        http_server.listen(self.ws_port)
        tornado.ioloop.IOLoop.instance().start()

    def get_subscribe_object(self):
        return self.subscribe_object

    def stop_consuming(self):
        print "Stopping subscription"
        self.subscribe_object.stop()

    def message_handler(self, message):
        parsed = decode_message(message)

        if parsed is not None:
            # Add to history so that it can be appended
            buffered_history.append((parsed.get_field('time'), parsed.get_field('message_content')))
            transmit_all_clients("[%s] (%s) %s" % (parsed.get_field('time'),
                                                   parsed.get_field('message_type'),
                                                   parsed.get_field('message_content')))
