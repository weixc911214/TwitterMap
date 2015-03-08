# -*- coding: utf-8 -*-
__author__ = 'wei'
import gevent.monkey
gevent.monkey.patch_all()
# import MySQLdb as sql
from flask import Flask, render_template,request
# from sqlalchemy import create_engine, MetaData, Table
import time
import tweepy
from flask_socketio import SocketIO, emit
from werkzeug.contrib.fixers import ProxyFix


application = Flask(__name__)
application.config["DEBUG"] = True
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)

import gevent
import gevent.queue
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets
sockets = Sockets(application)
seekers = gevent.queue.Queue()

def relay(from_, to):
    """route messges from_ -> to"""
    try:
        while True:
            to.send(from_.receive())
    except:
        # Notify to about disconnection - unless to disconnected
        try: to.send("Peer disconnected.")
        except: pass


def session(ws1, ws2):
    for ws in [ws1, ws2]:
        ws.send("/Found a person. Say hello")
    gevent.joinall([
        gevent.spawn(relay, ws1, ws2),
        gevent.spawn(relay, ws2, ws1)
    ])


def matcher(seekers):
    while True:
        gevent.spawn(session, seekers.get(), seekers.get())

gevent.spawn(matcher, seekers)

@sockets.route('/ws')
def websocket(ws):
    seekers.put(ws)
    ws.send("/Welcome. Seeking a partner")
    while True:  # hack to keep the greenlet alive
        gevent.sleep(0.5)

@application.route('/sockets')
def sockets():
    return render_template("socket.html")


application.wsgi_app = ProxyFix(application.wsgi_app)

#session = dict()
stream = object
keyword = "a"

consumer_key = "anbpwuMUw7nIlo5SXAxCU803j"

consumer_secret = "u2yVCFbi7os8dFrSUwmk4zzGRuyLMWkghHw1HcSiIMvSqHPp2p"

access_token = "761246203-hy3aSbOM1ct3dKc0MNLU15hUL3aeHSJrLSHKPBEK"
access_token_secret = "aqiOnSL0MG2KxSdcYuASJY8HuZq9svjLb4X97KSSFmvs2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@socketio.on('my event', namespace = '/test')
class Stream_Listener(tweepy.StreamListener):


    def on_status(self, status):

        if status.geo is None:
            return
        data = {}
        data['text'] = status.text
        data['created_at'] = time.mktime(status.created_at.timetuple())
        data['geo'] = { "lat" : status.geo["coordinates"][0], "lng": status.geo["coordinates"][1]}

        print data['geo']
        data['id'] = str(status.id)
        data['source'] = status.source


        global socketio

        emit('my event', {'data': data})
        #print data

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


@application.route('/message.html',methods=["GET", "POST"])
def message():
    if request.method == "POST":
        global keyword
        keyword = request.form["keyword"]
        print keyword
    # engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    # metadata = MetaData(bind=engine)
    # tweets = Table('TwitterMap', metadata, autoload = True)
    # result = tweets.select(tweets.c.text.like("%Columbia%")).execute().fetchall()
    result = []


    return render_template("message.html", data = result)


@socketio.on('my event', namespace = '/test')
def test_message(message):
    print message
    global socketio
    #print message
    # emit('my event', {'data': message})
    sl = Stream_Listener()

    stream = tweepy.Stream(auth=api.auth, listener=Stream_Listener())
    global keyword
    print "global keyword: %s" %keyword
    stream.filter(track=[keyword])
    #print "success"

import json
@application.route("/heatmap.html", methods=["GET", "POST"])
def heatmap():
    if request.method == "POST":
        global keyword
        keyword = request.form["keyword"]
        print keyword
    # engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    # metadata = MetaData(bind=engine)
    # tweets = Table('TwitterMap', metadata, autoload = True)
    # result = tweets.select(tweets.c.text.like("%Columbia%")).execute().fetchall()
    result = []
    return render_template("heatmap.html", data = result)



@application.route('/foundation')
def foundation():
    return render_template("foundation.html")


# def wsgi_app(environ, start_response):
#     path = environ["PATH_INFO"]
#     if path == "/":
#         return application(environ, start_response)
#     elif path == "/websocket":
#         handle_websocket(environ["wsgi.websocket"])
#     else:
#         return application(environ, start_response)
# def handle_websocket(ws):
#     while True:
#         message = ws.receive()
#         if message is None:
#             break
#         message = json.loads(message)
#         ws.send(json.dumps({'output': message['output']}))




if __name__ == "__main__":

    pywsgi.WSGIServer(('', 8000), application, handler_class=WebSocketHandler) \
          .serve_forever()
    # from gevent.pywsgi import WSGIServer
    # from geventwebsocket.handler import WebSocketHandler
    # http_server = WSGIServer(("localhost",8000), application, handler_class=WebSocketHandler)
    # print('Server started at %s:%s'%("localhost",8000))
    # http_server.serve_forever()
    # socketio.run(application, port=5000)





