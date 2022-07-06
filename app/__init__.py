from ctypes import util
import email
from email import utils
import imp
from importlib.metadata import metadata, requires
import firebase_admin
from flask import Config, Flask, jsonify,request
from itsdangerous import json
import requests
from firebase_admin import auth ,exceptions, storage, db, firestore, credentials 
from decouple import config
from .config.credentials import initialize
from .routes.home import home
from .routes.users import user
from .routes.notifications import noti
from .routes.products import products

app = Flask(__name__)

initialize(app)

app.register_blueprint(home)

app.register_blueprint(user)

app.register_blueprint(products)

app.register_blueprint(noti)