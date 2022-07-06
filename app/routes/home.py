from itertools import product
from optparse import Values
from typing import List
import flask
import firebase_admin
from firebase_admin import db

home = flask.Blueprint('home', __name__)

@home.route('/')
def homePage():
    return "Hello To Python-Flask Back-End FullMarket"