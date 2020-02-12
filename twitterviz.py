import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import tweepy
import datetime, time
import csv
from private import twitterkey, twittersecret, twitteraccesstoken, twittertokensecret

with open('wordlist.csv') as wordfile:
    reader = csv.reader(wordfile, delimiter="'")
    wordlist = list(reader)
    wordfile.close()
    print(wordlist)

auth = tweepy.OAuthHandler(twitterkey, twittersecret)
auth.set_access_token(twitteraccesstoken, twittertokensecret)
api = tweepy.API(auth)

def get_tweets(api, username):
    npage = 1
    deadend = False
    tweetlist = list()
    while True:
        tweets = api.user_timeline(username, page = npage)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 2:
                tweetlist.append([tweet.text.encode('UTF-8')])
                #print(tweet.created_at.strftime('%d-%b-%Y'), ' : ',  tweet.text.encode('UTF-8'))
            else:
                deadend = True
                print(tweetlist)
                return tweetlist

        if not deadend:
            npage  = npage + 1
            time.sleep(100)

tweetlist = get_tweets(api, 'IngrahamAngle')
print(tweetlist)




