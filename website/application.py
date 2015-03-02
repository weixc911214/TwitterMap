# -*- coding: utf-8 -*-
__author__ = 'wei'
import gevent.monkey
gevent.monkey.patch_all()
# import MySQLdb as sql
from flask import Flask, render_template
# from sqlalchemy import create_engine, MetaData, Table
import time
import tweepy
from flask_socketio import SocketIO, emit


application = Flask(__name__)
application.config["DEBUG"] = True
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)

session = dict()
stream = object


consumer_key = "anbpwuMUw7nIlo5SXAxCU803j"

consumer_secret = "u2yVCFbi7os8dFrSUwmk4zzGRuyLMWkghHw1HcSiIMvSqHPp2p"

access_token = "761246203-hy3aSbOM1ct3dKc0MNLU15hUL3aeHSJrLSHKPBEK"
access_token_secret = "aqiOnSL0MG2KxSdcYuASJY8HuZq9svjLb4X97KSSFmvs2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@socketio.on('my event', namespace='/test')
class Stream_Listener(tweepy.StreamListener):


    def on_status(self, status):

        # status.text, "\n"
        #print status.id
        #update(status.text)
        if status.geo is None:
            return
        data = {}
        data['text'] = status.text
        data['created_at'] = time.mktime(status.created_at.timetuple())
        data['geo'] = { "lat" : status.geo["coordinates"][0], "lng": status.geo["coordinates"][1]}

        print data['geo']
        data['id'] = str(status.id)
        data['source'] = status.source

        # self.channel.basic_publish(exchange='',
        #                             routing_key='twitter_topic_feed',
        #
        #                         body=json.dumps(data))
        #test_message
        #TweetsNamespace.broadcast('tweet_text', json.dumps(data))
        global socketio
        #def do():
        #test_message(data)
        #socketio.on('my event', namespace='/test')
        #socketio.emit('my event', {'data': data}, callback=self.ack())
        emit('my event', {'data': data})
        print data

        try:
            text = status.text.encode("utf8")
        except:
            return

        location = str(status.geo["coordinates"][0]) + "," + str(status.geo["coordinates"][1])


        tweet_id = status.id
        author_name = status.author.name
        author_id = status.author.id
        author_url = status.author.profile_image_url_https
        date = status.created_at
        # try:
        #
        #     db = sql.connect(host='cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com', user='weixc1234', passwd='wxc16888', db='innodb', cursorclass=sql.cursors.DictCursor)
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

    def ack(self):
        print 'message was received!'

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False




@application.route("/")
def index():
    # engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    # metadata = MetaData(bind=engine)
    # tweets = Table('TwitterMap', metadata, autoload = True)
    # result = tweets.select(tweets.c.text.like("%Columbia%")).execute().fetchall()
    result = []
    return render_template("index.html", data = result)

    # for r in result:
    #     print type(r["text"])


@application.route('/message.html')
def message():
    # engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    # metadata = MetaData(bind=engine)
    # tweets = Table('TwitterMap', metadata, autoload = True)
    # result = tweets.select(tweets.c.text.like("%Columbia%")).execute().fetchall()
    result = []
    # for r in result:
    #     print type(r["text"])

    return render_template("message.html", data = result)


@socketio.on('my event', namespace='/test')
def test_message(message):
    print message
    global socketio
    #print message
    # emit('my event', {'data': message})
    sl = Stream_Listener()

    stream = tweepy.Stream(auth=api.auth, listener=Stream_Listener())

    stream.filter(track=['a'])
    #print "success"


@application.route("/heatmap.html")
def heatmap():
    # engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    # metadata = MetaData(bind=engine)
    # tweets = Table('TwitterMap', metadata, autoload = True)
    # result = tweets.select(tweets.c.text.like("%Columbia%")).execute().fetchall()
    result = []
    return render_template("heatmap.html", data = result)



if __name__ == "__main__":
    # t = threading.Thread(target=ping_thread)
    # t.daemon = True
    # t.start()
    application.run()
    # socketio.run(application)
    # SocketIOServer(('', 5000), app, resource="socket.io").serve_forever()




