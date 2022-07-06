import decouple
import firebase_admin
import flask_cors
import requests
import flask_cors
import cloudinary


def initialize(app):
    cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    url = decouple.config('URLCredentialKey')
    headers = {
      'X-Master-Key': decouple.config('KeyCredentialJSON')
    }
    
    req = requests.get(url, json=None, headers=headers)
    
    data = req.json()['record']
    
    cred = firebase_admin.credentials.Certificate(data)
    
    startDB = firebase_admin.initialize_app(cred, {
        'databaseURL': decouple.config('DBURL'),
    })

    cloudinary.config( 
        cloud_name = decouple.config('CLOUDNAME'), 
        api_key = decouple.config('KEYVALUECLOUD'), 
        api_secret = decouple.config('SECRETKEYCLOUD'),
        secure = True
    )