from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from textblob import TextBlob
import pandas as pd
import numpy as np
import re

import private

#### Twitter Client ####
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticatetwitterapp()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def home_timeline_tweets(self, num_tweets):
        home_tweets = []
        for hometweets in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_tweets.append(hometweets)
        return home_tweets

#### Twitter Authenticator ####
class TwitterAuthenticator():
    def authenticatetwitterapp(self):
        auth = OAuthHandler(private.twitterkey, private.twittersecret)
        auth.set_access_token(private.twitteraccesstoken, private.twittertokensecret)
        return auth


class TwitterStreamer():
    """" Class for streaming and processing live tweets"""
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def streamtweets(self, fetchedtweetsfile, hashtaglist):
        # This handles authentication and connection to the API
        listener = TwitterListener(fetchedtweetsfile)
        auth = self.twitter_authenticator.authenticatetwitterapp()
        stream = Stream(auth, listener)
        stream.filter(track = hashtaglist)


class TwitterListener(StreamListener):
    """This is a basic listener ethat just prints received tweets to stdout"""

    def __init__(self,fetchedtweetsfile):
        self.fetchedtweetsfile = fetchedtweetsfile


    def on_data(self, data):
        try:
            with open(self.fetchedtweetsfile, 'a') as tf:
                tf.write(data)
            print(data)
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # returning false on_data method in case rate limit occurs
            return False
        print(status)

class TweetAnalyzer():
    """
    functionality for analyzing and categorizing content from tweets
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet for tweet in tweets])
        df['retweetcount'] = np.array([tweet.retweet_count for tweet in tweets])
        df['favorites'] = np.array([tweet.favorite_count for tweet in tweets])
        df['user'] = np.array([tweet.user.name for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        return df

if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name=['seanhannity', 'maddow'], count=200)

    #print(tweets[0].retweet_count)
    #print(tweets[0].id)
    df = tweet_analyzer.tweets_to_dataframe(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))






    #print(df.head(5))
    # prints field list
    # print(dir(tweets[0]))




