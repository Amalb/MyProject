import pandas as pd
import time
import re
from pymongo import MongoClient
from textblob import TextBlob

connection = MongoClient('localhost', 27017)
db = connection.twitter_db
# get todays tweets function
data = db.tweets
today = time.strftime("%a %b %d")
tweets_list = []
tweets_iterator = data.find({'created_at': {'$regex': today}}, {'text': 1})
print("tweets imported from mongo")
# creating a list of tweets from the tweets iterator
for tweet in tweets_iterator:
    tweets_list.append(tweet)
tweets = pd.DataFrame()
tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_list))


def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def sentiment_analysis ():
    sentimentlist = []
    sentiment_tweets = []

    for index, tweet in tweets.iterrows():
        parsed_tweet = {}
        parsed_tweet['text'] = str(tweet['text'])
        parsed_tweet['sentiment']=get_tweet_sentiment(str(tweet["text"]))
        sentiment_tweets.append(parsed_tweet)

    ptweets = [tweet for tweet in sentiment_tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(sentiment_tweets)))
    pos_value = float("{0:.2f}".format(100 * len(ptweets) / len(sentiment_tweets)))
    sentimentlist.append(pos_value)
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in sentiment_tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(sentiment_tweets)))
    neg_value = float("{0:.2f}".format(100 * len(ntweets) / len(sentiment_tweets)))
    sentimentlist.append(neg_value)
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets)) ) / len(sentiment_tweets)))
    neu_value = float("{0:.2f}".format(100 * (len(tweets) - (len(ntweets) + len(ptweets)) ) / len(sentiment_tweets)))
    sentimentlist.append(neu_value)
    # printing first 5 positive tweets
    # print("\n\nPositive tweets:")
    # for tweet in ptweets[:10]:
    #     print(tweet['text'])
    #
    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for tweet in ntweets[:10]:
    #     print(tweet['text'])
    return sentimentlist

