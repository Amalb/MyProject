import pandas as pd
import time

import re
from pymongo import MongoClient
from textblob import TextBlob


def main():


    connection = MongoClient('localhost', 27017)
    db = connection.twitter_db
    # get todays tweets function
    data = db.tweets
    today = time.strftime("%a %b %d")
    tweets_list = []
    tweets_iterator = data.find({'created_at': {'$regex': today}})
    tweets = pd.DataFrame()
    print("tweets imported from mongo")
# creating a list of tweets from the tweets iterator
    for tweet in tweets_iterator:
        tweets_list.append(tweet)
    print(tweets_list[1])

if __name__ == "__main__":
    # calling main function
    main()
