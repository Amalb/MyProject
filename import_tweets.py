import sys
import json
import time
from http.client import IncompleteRead
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials


# start timer
startTime = time.time()


# This is a basic listener that just prints received tweets to stdout.
class MyStreamListener(StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streamingAPI.")

    # initialise values of the class
    def __init__(self, api=None):
        self.counter = 0
        self.limittime = 1

    def on_data(self, data):

        try:

            datajson = json.loads(data)
            # Store tweet info into the collection.
            credentials.coll.insert(datajson)
            # increase the tweets counter by one
            self.counter = self.counter + 1
            # print (self.counter, ") ", datajson["text"].encode("utf-8"))
            # print ("\n\n")

        except KeyError:
            # catch any Key encode error from json document
            print
            "Print Key Error"

        # check time for termination conditions
        if (time.time() - startTime) >= ((self.limittime * 24 * 60 * 60)):
            credentials.client.close()
            print
            "elapsed time in minutes", (time.time() - startTime) / 60
            sys.exit(0)

    def on_error(self, status_code):
        print("status code", status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        return True  # Don't kill the stream


def streaming(keywords):
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = MyStreamListener()
    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)

    while True:
        try:
            stream = Stream(auth, l)
            # This line filter Twitter Streams to capture data by the keyword-s
            if (keywords == "terrorism"):
                stream.filter(track=credentials.terrorism_keywords,stall_warnings=True,  async=True, languages=['en','fr','ar'])
            elif (keywords == "sport"):
                stream.filter(track=credentials.sport_keywords, stall_warnings=True, async=True, languages=['en','fr','ar'])

            else:
                stream.filter(track=credentials.news_keywods, stall_warnings=True, async=True, languages=['en','fr','ar'])

        except IncompleteRead:
            continue
            # Oh well, reconnect and keep trucking

        except KeyboardInterrupt:
            stream.close()

# sys.exit(0)
