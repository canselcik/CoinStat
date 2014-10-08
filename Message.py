import json
import time


class Message:
    def __init__(self, message_type, message_content):
        self.container = dict()
        self.add_field('message_type', message_type)
        self.add_field('message_content', message_content)
        self.add_field('time', int(time.time()))

    def replace_container(self, new_container):
        self.container = new_container

    def add_field(self, field, val):
        if field in self.container:
            return False
        else : 
            self.container[field] = val
            return True 

    def set_field(self, field, val):
        if field not in self.container:
            return False
        self.container[field] = val
        return True

    def get_field(self, field):
        if field not in self.container:
            return None
        return self.container[field]

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
        return self.get_field('time')

    def get_body(self):
        return self.get_field('message_content')

    def get_type(self):
        return self.get_field('message_type')


def decode_message(string_representation):
    try:
        json_dict = json.loads(string_representation)
        m = Message("", "")
        m.replace_container(json_dict)
        return m
    except ValueError:
        print "An error occurred while decoding the incoming string"
        return None