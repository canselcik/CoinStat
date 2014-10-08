#!/usr/bin/python
from tweepy import Stream
import string
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from Producer import Producer
from Message import *
import json
import operator
from textblob import TextBlob

ckey = 'ypoD0SpeR9wTnBakqYqsGqnLi'
csecret = 'RUY6OFwZX4GKXHmoQsU023SuwRGAUBHyrURa9HIUOCehQEz7o4'
atoken = '2845320649-qYLFU09FUwJ4VMsfjiCqgRCJu120OYVuYCDbVpc'
asecret = 'amCBzAKFk7ILALGM9haSYnSbI4WmsxcxFZ4bTFMXraSH3'
#keywords = ["bitcoin", "btc", "bitstamp", "bitfinex"]
keywords = ["grubhub"]
diff_time = 10
print_each = True

host = "amqp://cselcik.com"
exchange = "updates"
routing_type = "direct"
routing_key = ""

# All arguments are strings
p = Producer(host, exchange, routing_type, routing_key)

def broadcast(p, message_text, pos, neg):
    m = Message("twitter"   , message_text  )
    m.add_field("pos_sent"  , str(pos)      )
    m.add_field("neg_sent"  , str(neg)      )
    p.send(m.str())
    print "SENT " + m.str()

'''
class Interpreter:
    def __init__(self):
        self.histogram = {}
        self.sorted_hist = []

    def add_word(self, sentence):
        words = sentence.split(' ')
        for w in words:
            if w not in self.histogram:
                self.histogram[w] = 0
            self.histogram[w] += 1
   
    def sort_histogram(self):
        self.sorted_hist = sorted(self.histogram.items(), key=operator.itemgetter(1))
    
    def dump_histogram(self):
        self.sort_histogram()
        stropt = ''
        for item in self.sorted_hist:
            filtered_key = item[0].encode('ascii', errors='ignore')
            filtered_val = str(item[1]).encode('ascii', errors='ignore')
            stropt = stropt + "\n" + filtered_key + " = " + filtered_val
        f = open('output.txt', 'a')
        f.write(stropt)
        f.close()
'''

class listener(StreamListener):
    def __init__(self):
        self.counter = 0
        self.last_sent = time.time()
        self.pos_sent_polarity = 0.0
        self.neg_sent_polarity = 0.0

    def on_data(self, data):
        structured = json.loads(data)
        if 'text' not in structured:
            return False
        #if 'RT' not in structured or structured['RT'] == 'true':
        #    return False


        blob = TextBlob(structured['text'])
        dur_sent = blob.sentiment.polarity
        if dur_sent < 0.0 : 
            self.neg_sent_polarity += dur_sent
        else: 
            self.pos_sent_polarity += dur_sent

        if print_each :
            print "[%d] %s polarity = %s" % (self.counter, structured['text'], str(dur_sent))
          
        self.counter += 1
        if time.time() - self.last_sent > diff_time:
            self.last_sent = time.time()
            broadcast(p, str(self.counter), self.pos_sent_polarity, self.neg_sent_polarity)
            self.pos_sent_polarity = 0.0
            self.neg_sent_polarity = 0.0
            self.counter = 0
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=keywords)

