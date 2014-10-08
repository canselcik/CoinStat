#!/usr/bin/python
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from Producer import Producer
from Message import *
import json
#import operator
#from textblob import TextBlob

ckey = 'ypoD0SpeR9wTnBakqYqsGqnLi'
csecret = 'RUY6OFwZX4GKXHmoQsU023SuwRGAUBHyrURa9HIUOCehQEz7o4'
atoken = '2845320649-qYLFU09FUwJ4VMsfjiCqgRCJu120OYVuYCDbVpc'
asecret = 'amCBzAKFk7ILALGM9haSYnSbI4WmsxcxFZ4bTFMXraSH3'

keywords = ["bitcoin", "btc", "bitstamp", "bitfinex"]

diff_time = 60

host = "amqp://cselcik.com"
exchange = "updates"
routing_type = "direct"
routing_key = ""


class TwitterStreamListener(StreamListener):
    def __init__(self):
        print "TwitterStreamListener started"
        self.counter = 0
        self.last_sent = time.time()
        self.producer = Producer(host, exchange, routing_type, routing_key)
        #self.pos_sent_polarity = 0.0
        #self.neg_sent_polarity = 0.0

    def broadcast(self, message_text): #, pos, neg):
        if self.producer is None:
            print "Cannot send because self.producer is None"
            return False

        m = Message("twitter-volume", message_text)
        #m.add_field("pos_sent", str(pos))
        #m.add_field("neg_sent", str(neg))

        if self.producer.send(m.str()):
            print "[%d] Transmission successful" % m.get_time()
        else:
            print "[%d] Transmission failed" % m.get_time()

    def on_data(self, data):
        structured = json.loads(data)
        if 'text' not in structured:
            return True

        print "Received tweet with keyword (counter=%d)" % self.counter

        #blob = TextBlob(structured['text'])
        #dur_sent = blob.sentiment.polarity
        #if dur_sent < 0.0:
        #    self.neg_sent_polarity += dur_sent
        #else:
        #    self.pos_sent_polarity += dur_sent

        #if print_each:
        #    print "[%d] %s polarity = %s" % (self.counter, structured['text'], str(dur_sent))
          
        self.counter += 1
        if time.time() - self.last_sent > diff_time:
            self.last_sent = time.time()
            self.broadcast(str(self.counter)) # self.pos_sent_polarity, self.neg_sent_polarity)
            #self.pos_sent_polarity = 0.0
            #self.neg_sent_polarity = 0.0
            self.counter = 0
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, TwitterStreamListener())
twitterStream.filter(track=keywords)

