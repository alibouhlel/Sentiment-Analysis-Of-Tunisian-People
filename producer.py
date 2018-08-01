import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from kafka import KafkaProducer


# import twitter keys and tokens
from config import *

#initiliase the kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)

        # delete some fields
        if 'extended_entities' in dict_data:
            del dict_data["extended_entities"]
        if 'retweeted_status' in dict_data:
            del dict_data["retweeted_status"]
        if 'quoted_status' in dict_data:
            del dict_data["quoted_status"]

        # pass tweet into TextBlob in order to calculate it's polarity
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

        # add sentiment and polarity to data

        dict_data["sentiment"]=sentiment
        dict_data["polarity"]=tweet.sentiment.polarity

        #dumps dict_data in order to send it to kafka topic

        message=json.dumps(dict_data)

        #send the data to kafka the message must be a byte that's why it's encoded

        producer.send(KAFKA_TOPIC, message.encode('utf-8'))
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
stream.filter(locations=GEOBOX_TUNISIA)
