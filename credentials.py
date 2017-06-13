#Variables that contains the user credentials to access Twitter API
import time
from pymongo import MongoClient

# Variables that contains the user credentials to access Twitter API
access_token = "712782833656471552-d0K1viS20yVRWvMeYWgbv7A6ECf7qhF"
access_token_secret = "aqNsNsKe6b4NRg8TCR2RB9gBiTx9a0thr4NFu6E6iFmri"
consumer_key = "FanPBOeBV9bSBN5r1n3KqPX2X"
consumer_secret = "hhma709vs1nZ5TPikReZA2pwvS6PvmUXrZwuVNhwHDXqmtLRMh"

# connect to mongoDB
client = MongoClient("127.0.0.1:27017")
db = client.twitter_db
coll = db['tweets']
#start timer
startTime = time.time()

#keyword to filter from twitter
terrorism_keywords = ['terrorist', 'terrorism', 'attack', 'bombe', 'attaque', 'daech', 'isis']
sport_keywords=['football','tennis','rolandgarros','Champions League','Hockey','Gymnastics','Baseball','soccer','NHL','NFL']
news_keywods=['news', 'world', 'monde']


mystop = {'say','see','make','like','want','know','vote','must','well','still','super','notifications','','re', 'rt', 'retweet', '#fuckem', '#fuck', 'fuck', 'ya', 'yall', 'yay', 'youre', 'youve', 'ass', 'factbox',
         'com', 'lt', 'th', 'retweeting', 'dick', 'fuckin', 'shit', 'via', 'fucking', 'shocker', 'wtf', 'hey', 'ooh',
         '#retweet', 'retweet', 'go', 'hellooo', 'gooo', 'fucks', 'fucka', 'bitch', 'wey', 'im', 'fucking', 'got',
         'sooo', 'hello', 'amp', 'to', 'best', 'care', 'bill', 'try', 'team', 'would', 'think', 'new',
          'like', 'video', 'dont', 'times', 'media', 'u', 'insurance', 'please','tell', 'rights','price',
          }