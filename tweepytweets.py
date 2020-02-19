from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import private

class TwitterStreamer():
    """" Class for streaming and processing live tweets"""
    def __init__(self):
        pass

    def streamtweets(self, fetchedtweetsfile, hashtaglist):
        # This handles authentication and connection to the API
        listener = StdOutListener(fetchedtweetsfile)
        auth = OAuthHandler(private.twitterkey, private.twittersecret)
        auth.set_access_token(private.twitteraccesstoken, private.twittertokensecret)
        stream = Stream(auth, listener)
        stream.filter(track = hashtaglist)


class StdOutListener(StreamListener):
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
        print(status)

if __name__ == '__main__':
    hashtags = ['trump', 'gutfield', 'bernie sanders']
    fetchedtweetsfile = 'tweetfile.json'
    twitter_streamer = TwitterStreamer()
    twitter_streamer.streamtweets(fetchedtweetsfile, hashtags)



