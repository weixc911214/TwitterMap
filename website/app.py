# -*- coding: utf-8 -*-
__author__ = 'wei'

from flask import Flask, jsonify, render_template, request, abort
from sqlalchemy import create_engine, MetaData, Table
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from database import db_session
import message

from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config["DEBUG"] = True
msgsrv = message.MessageServer()

@app.route("/")
def index():
    engine = create_engine('mysql://weixc1234:wxc16888@cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com/innodb', convert_unicode=True)
    metadata = MetaData(bind=engine)
    tweets = Table('TwitterMap', metadata, autoload = True)
    result = tweets.select(tweets.c.text.like("%Starbucks%")).execute().fetchall()

    for r in result:
        print type(r["text"])
    #geo = result["geo"].encode('utf-8')

    return render_template("index.html", data = result)

@app.route('/message/')
def message():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        msgsrv.observers.append(ws)
        while True:
            if ws.socket:
                message = ws.receive()
                if message:
                    msgsrv.add_message("%s" % message)
            else:
                abort(404)
    return "Connected!"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
