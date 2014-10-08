import json
import time


def decode_message(string_representation):
    try:
        json_dict = json.loads(string_representation)
        m = Message("", "")
        m.replace_container(json_dict)
        return m
    except ValueError:
        print "An error occured while decoding the incoming string"
        return None

class Message:
    def __init__(self, message_type, message_content):
        self.container = dict()
        self.container['message_type'] = message_type
        self.container['message_content'] = message_content
        self.container['time'] = int(time.time())
        pass

    def replace_container(self, new_container):
        self.container = new_container

    def str(self):
        if self.container is None:
            return None
        try:
            string_rep = json.dumps(self.container)
            return string_rep
        except ValueError:
            print "An error occurred while dumping JSON data"
            return None

    def get_time(self):
        if self.container is None or 'time' not in self.container:
            return None
        return self.container['time']

    def get_body(self):
        if self.container is None or 'message_content' not in self.container:
            return None
        return self.container['message_content']

    def get_type(self):
        if self.container is None or 'message_type' not in self.container:
            return None
        return self.container['message_type']