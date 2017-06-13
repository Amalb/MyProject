import time
import pandas as pd
from pymongo import MongoClient
import string
import nltk
from nltk.corpus import stopwords
import numpy as np
import lda
from sklearn.feature_extraction.text import CountVectorizer
from credentials import mystop
from nltk.tokenize import TweetTokenizer

connection = MongoClient('localhost', 27017)
db = connection.twitter_db
# get todays tweets function
data = db.tweets
today = time.strftime("%a %b %d")
tweets_list = []
tweets_iterator = data.find({'created_at': {'$regex': today}}, {'text': 1, 'created_at': 1})
# creating a list of tweets from the tweets iterator
for tweet in tweets_iterator:
    tweets_list.append(tweet)
tweets = pd.DataFrame()
print("tweets uploaded")
# creating a dataframe of tweets
tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_list))
tweets['created_at'] = list(map(lambda tweet: tweet['created_at'], tweets_list))  # convert created_at to datetimes
stop = stopwords.words('english') + stopwords.words('french')

df = tweets
temp_df = df.copy()
print("cleaning tweets")

# Remove hyperlinks
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('http\S+', '', regex=True)
# Remove hashtags
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('#', ' ', regex=True)
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('amp', ' ', regex=True)

temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('rt\w*', ' ', regex=True)
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('RT\w*', ' ', regex=True)
# Remove citations
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('\@\w*', '', regex=True)
# Remove tickers
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('\$\w*', '', regex=True)
# Remove punctuation
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('[' + string.punctuation + ']+', '', regex=True)
# Remove quotes
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('&\w*', '', regex=True)
# Remove RT
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('\s+rt\s+', '', regex=True)
# Remove linebreak, tab, return
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('[\n\t\r]+', ' ', regex=True)
# Remove via with blank
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('via+\s', '', regex=True)
# Remove multiple whitespace
temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('\s+\s+', ' ', regex=True)
# Remove stopwords
tweet_tokenized = []

for tweet in temp_df.loc[:, "text"]:
    tweet_tokenized = nltk.word_tokenize(tweet)

print("deleting stop words")
s = 0
for w in tweet_tokenized:
    if (w in stop) | (w in mystop):
        # temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace('[\W*\s?\n?]' + w + '[\W*\s?]', ' ', regex=True)
        temp_df.loc[:, "text"] = temp_df.loc[:, "text"].replace(w, '')
        s = s + 1

        # print("w in stopword")
print(s)
tweets = temp_df

# transform GMT timezone to Europe Paris
# creates new timestamp on the left of the dataframe
tweets['created_at'] = pd.to_datetime(pd.Series(tweets['created_at']))
tweets.set_index('created_at', drop=False, inplace=True)
tweets.index = tweets.index.tz_localize('GMT').tz_convert('Europe/Paris')
tweets.index = tweets.index - pd.DateOffset(hours=24)
# created_at timeseries in a per minute minute format
tweets1m = tweets['created_at'].resample('1t').count()
# average tweets per minute
# avg = tweets1m.mean()

text = tweets['text']
tokens = []
for txt in text.values:
    tokens.extend([t.lower().strip(":,.") for t in txt.split()])
filteredtokens = tokens

# compute frequency distribution
freqdist = nltk.FreqDist(filteredtokens)
# find 100 most frequent words
freqdist = freqdist.most_common(50)
print(freqdist)

tokens = {}

for i in range(len(filteredtokens)):
    tokens[i] = filteredtokens[i]

len(tokens)

# Words occurring in only one document or in at least 95% of the documents are removed.

tf = CountVectorizer(strip_accents='unicode', max_df=0.97, min_df=2, stop_words=stop)
tfs1 = tf.fit_transform(tokens.values())
num = 4
model = lda.LDA(n_topics=num, n_iter=100, random_state=1)

# Document Term Matrix structure
model.fit_transform(tfs1)

# Obtain the words with high probabilities
topic_word = model.topic_word_

# Obtain the feature names
vocab = tf.get_feature_names()
events_words = []
# choose how many words per topic
n_top_words = 8


def get_events():
    try:
        for i, tokens in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(tokens)][:-n_top_words:-1]
            events_words.append(' '.join(topic_words))
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    except:
        pass

    return events_words


# get the topic of each tweet (text[i])
doc_topic = model.doc_topic_

for i in range(10):
    print("{} (top topic: {})".format(text[i], doc_topic[i].argmax()))
