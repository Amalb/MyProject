from httplib import IncompleteRead
import sys
import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

#Variables that contains the user credentials to access Twitter API
access_token = "712782833656471552-d0K1viS20yVRWvMeYWgbv7A6ECf7qhF"
access_token_secret = "aqNsNsKe6b4NRg8TCR2RB9gBiTx9a0thr4NFu6E6iFmri"
consumer_key = "FanPBOeBV9bSBN5r1n3KqPX2X"
consumer_secret = "hhma709vs1nZ5TPikReZA2pwvS6PvmUXrZwuVNhwHDXqmtLRMh"

#connect to mongoDB
client = MongoClient("127.0.0.1:27017")
db = client.twitter_db
coll = db['tweets']

#start timer
startTime = time.time()

#keyword to filter from twitter
terrorism_keywords = ['terrorist', 'terrorism', 'attack', 'bombe', 'attaque', 'daech', 'isis']
sport_keywords=['football','tennis','rolandgarros','Champions League','Hockey','Gymnastics','Baseball','soccer','NHL','NFL']
news_keywods=['news', 'world', 'monde']
#This is a basic listener that just prints received tweets to stdout.
class MyStreamListener(StreamListener):

# This is a class provided by tweepy to access the Twitter Streaming API.
   def on_connect(self):
       # Called initially to connect to the Streaming API
       print("You are now connected to the stre amingAPI.")

#initialise values of the class
   def __init__(self, api=None):
       self.counter = 0
       self.limittime=1


   def on_data(self, data):

       # Decode JSON
       #datajson = json.loads(data)

       try:

            datajson = json.loads(data)
            # Store tweet info into the collection.
            coll.insert(datajson)
            #increase the tweets counter by one
            self.counter = self.counter + 1
            #print text only
            print self.counter, ") ", datajson["text"].encode("utf-8")
            print "\n\n"

       except KeyError:
           #catch any Key encode error from json document
           print "Print Key Error"

       #check time for termination conditions
       if (time.time() - startTime) >= ((self.limittime * 24 * 60 * 60) ):
           client.close()
           print "elapsed time in minutes", (time.time() - startTime)/60
           sys.exit(0)


   def on_error(self, status_code):
       print("status code", status_code)
       return True # Don't kill the stream


   def on_timeout(self):
       return True # Don't kill the stream



def streaming(keywords):
   #This handles Twitter authetification and the connection to Twitter Streaming API
   l = MyStreamListener()
   auth = OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)

   while True:
       try:
           stream = Stream(auth, l)
           #This line filter Twitter Streams to capture data by the keyword-s
           if (keywords=="terrorism"):
                stream.filter(track=terrorism_keywords, stall_warnings=True)
           elif (keywords=="sport"):
               stream.filter(track=sport_keywords, stall_warnings=True)
           else :
               stream.filter(track=news_keywods, stall_warnings=True)

       except IncompleteRead:
           pass
           # Oh well, reconnect and keep trucking

       except KeyboardInterrupt:
           stream.close()
#sys.exit(0)

