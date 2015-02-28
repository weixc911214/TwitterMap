__author__ = 'wei'
import tweepy
import json
import MySQLdb as sql
import MySQLdb.cursors
class Stream_Listener(tweepy.StreamListener):
from  website import message
    def on_status(self, status):
        msg = message.MessageServer()

        # tweet_id = status.id
        #
        # if status.geo is None:
        #     return
        #
        # #print "hello"
        # try:
        #     text = status.text.encode("utf8")
        # except:
        #     return
        #
        # location = str(status.geo["coordinates"][0]) + "," + str(status.geo["coordinates"][1])
        #
        #
        #     #print "aaa"
        # #print geo
        # #print type(text)
        # author_name = status.author.name
        # author_id = status.author.id
        # author_url = status.author.profile_image_url_https
        # date = status.created_at
        # try:
        #     db = sql.connect(host='cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com', user='weixc1234', passwd='wxc16888', db='innodb', cursorclass=MySQLdb.cursors.DictCursor)
        #     cursor = db.cursor()
        #     #print geo
        #     test_sql ="""INSERT INTO innodb.TwitterMap(id, text, geo, author_name, author_id, author_url, date) VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")""" % (str(tweet_id), text, location, author_name, str(author_id), author_url, date)
        #     #print test_sql
        #     cursor.execute(test_sql)
        #     db.commit()
        #     db.close()
        #     print "success"
        #     #print test_sql
        # except:
        #     pass



    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

consumer_key = "anbpwuMUw7nIlo5SXAxCU803j"

consumer_secret = "u2yVCFbi7os8dFrSUwmk4zzGRuyLMWkghHw1HcSiIMvSqHPp2p"

access_token = "761246203-hy3aSbOM1ct3dKc0MNLU15hUL3aeHSJrLSHKPBEK"
access_token_secret = "aqiOnSL0MG2KxSdcYuASJY8HuZq9svjLb4X97KSSFmvs2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

sl = Stream_Listener()

myStream = tweepy.Stream(auth=api.auth, listener=Stream_Listener())

myStream.filter(track=['Nike'])

