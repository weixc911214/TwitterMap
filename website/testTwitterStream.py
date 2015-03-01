__author__ = 'wei'
import tweepy

from flask import Flask, jsonify, render_template, request, abort, session
from flask_socketio import SocketIO, emit
import pika
import json
thread = None
import time
from flask import copy_current_request_context
from app import update








