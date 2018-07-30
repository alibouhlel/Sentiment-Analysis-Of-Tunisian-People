import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch

# import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch()


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)
        if 'extended_entities' in dict_data:
            del dict_data["extended_entities"]
        if 'retweeted_status' in dict_data:
            del dict_data["retweeted_status"]
        if 'quoted_status' in dict_data:
            del dict_data["quoted_status"]



        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])

        # output sentiment polarity
        print tweet.sentiment.polarity

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # add sentiment field to data

        dict_data["sentiment"]=sentiment
        dict_data["polarity"]=tweet.sentiment.polarity


        # add tweet's data and sentiment info to elasticsearch
        es.index(index="last",
                 doc_type="test-type",
                 body=dict_data)
        return True

    # on failure
    def on_error(self, status):
        print status

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for tunisian's related keywords
stream.filter(track=['tunisia'])
