__author__ = 'wei'
import tweepy

consumer_key = "anbpwuMUw7nIlo5SXAxCU803j"

consumer_secret = "u2yVCFbi7os8dFrSUwmk4zzGRuyLMWkghHw1HcSiIMvSqHPp2p"

access_token = "3154095670-KzH1kiSRcMnObQhIkTcxLzbL8HnTSYEruOGYRhW"
access_token_secret = "vMM6yOJLvVUpLxRf6W0qW2ImIS2tA1Ky9QbMiIA63r7VZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search("columbia")
for tweet in public_tweets:
    print tweet.text
