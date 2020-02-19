from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import private

#### Twitter Client ####
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticatetwitterapp()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

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

if __name__ == '__main__':
    hashtags = ['trump', 'gutfield', 'bernie sanders']
    fetchedtweetsfile = 'tweetfile.json'
    twitter_client = TwitterClient('kattimpf')
    print(twitter_client.get_user_timeline_tweets(2))

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.streamtweets(fetchedtweetsfile, hashtags)



