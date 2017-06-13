import pandas as pd
import time

import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.twitter_db
# get todays tweets function
data = db.tweets
today = time.strftime("%a %b %d")
tweets_list = []
tweets_iterator = data.find({'created_at': {'$regex': today}}, {'screen_name': 1,'retweet_count': 1,'favorite_count': 1}).sort("retweet_count",pymongo.DESCENDING)

print("tweets imported from mongo")
# creating a list of tweets from the tweets iterator
for tweet in tweets_iterator:
    tweets_list.append(tweet)
print (tweets_list)
