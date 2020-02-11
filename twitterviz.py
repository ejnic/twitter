import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import tweepy
import private
import datetime, time
from private import twitterkey, twittersecret, twitteraccesstoken, twittertokensecret

auth = tweepy.OAuthHandler(twitterkey, twittersecret)
auth.set_access_token(twitteraccesstoken, twittertokensecret)
api = tweepy.API(auth)

def get_tweets(api, username):
    npage = 1
    deadend = False
    while True:
        tweets = api.user_timeline(username, page = npage)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 7:
                print(tweet.created_at.strftime('%d-%b-%Y'), ' : ',  tweet.text.encode('UTF-8'))
            else:
                deadend = True
                return

        if not deadend:
            npage  = npage + 1
            time.sleep(100)

get_tweets(api, 'IngrahamAngle')





