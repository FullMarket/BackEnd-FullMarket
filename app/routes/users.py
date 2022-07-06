from lib2to3.pgen2 import token
import flask
import firebase_admin
from firebase_admin import auth, db
import cloudinary
import cloudinary.uploader
import passlib
from passlib.hash import pbkdf2_sha256
import jose
from jose import jwt
import decouple
import urllib.parse

user = flask.Blueprint('user', __name__)

def UploadFiles(file, nameU, filename): 
    LoadFile = cloudinary.uploader.upload(file, folder = f"photoUsers/{nameU}", public_id = filename)
    return LoadFile['url']

def DeleteOrPutFiles(publicid):
    Delete = cloudinary.uploader.destroy(publicid)
    return Delete

def EncryptPassword(password):
    EncryptWithPasslib = pbkdf2_sha256.hash(password)
    HashEncondeMore = EncryptWithPasslib[::-1]
    tokenHash = jwt.encode({'key': HashEncondeMore}, decouple.config('ENCODE') , algorithm='HS256')
    return tokenHash

def DecryptPassword(password, token):
    tokenDecode = jwt.decode(token, decouple.config('ENCODE'), algorithms=['HS256'])
    tokenGetKey = tokenDecode['key'] #Esta en parametro 
    HashDecodeMore = tokenGetKey[::-1]
    Decryptpass = pbkdf2_sha256.verify(password, HashDecodeMore)
    return Decryptpass

@user.route("/users/createuser", methods = ["POST"])

def PostToRegisterUser():
    name = flask.request.form.get('name')
    alias = flask.request.form.get('alias')
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    department = flask.request.form.get('department')
    municipality = flask.request.form.get('municipality') 
    address = flask.request.form.get('address')
    phone = flask.request.form.get('phone')
    photo = flask.request.files.get('photo')

    passwordEncrypt = EncryptPassword(password)
    user = auth.create_user(email = email, password = password)
    imgUserURL = UploadFiles(photo, name , photo.filename)
    userToDB = db.reference('/users').child(user.uid).set({
        'name': name,
        'alias': alias,
        'email': email,
        'password': passwordEncrypt,
        'department': department,
        'municipality': municipality,
        'address': address,
        'phone': phone,
        'photo': imgUserURL
    })
    return "User Create"

@user.route("/users/login", methods = ["POST"])
def GetUserToLogin():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    user = auth.get_user_by_email(email)
    print(email)
    print(password)
    if user:
        dataUser = db.reference('/users').child(user.uid).get() #Traer datos
        passwordEncrypted = dataUser['password']
        passDecode = DecryptPassword(password, passwordEncrypted) #Me voy a matar, yo pensando que era una lista
        if  passDecode: 
            token = auth.create_custom_token(user.uid, dataUser)
            return flask.jsonify({
                'token' : str(token).replace('b', '', 1)
                })
        else:
            return "The password is Invalid"
    else:
        return "Object Invalid"


@user.route("/users/edituser/<string:uid>", methods = ["PUT"])
def editProfileUser(uid):
    user = {
        'name': flask.request.form.get('name'),
        'alias': flask.request.form.get('alias'),
        'email': flask.request.form.get('email'),
        'password': flask.request.form.get('password'),
        'department': flask.request.form.get('department'), 
        'municipality': flask.request.form.get('municipality'),
        'address': flask.request.form.get('address'),
        'phone': flask.request.form.get('phone'),
        # 'photo': flask.request.files.get('photo'),
    }
    getUser = db.reference('/users').child(uid).update(user)
    return "User Updated"

@user.route("/users/deleteuser/<string:uid>", methods = ["DELETE"])
def deleteUserById(uid):
    urlimgUser = db.reference('/users').child(uid).get()['photo']
    urlimgDecode = urllib.parse.unquote(urlimgUser)
    db.reference('/users').child(uid).set({})
    positionFileUers = urlimgDecode.find('photoUsers')
    img = urlimgDecode[positionFileUers: -4]
    imgDelete = DeleteOrPutFiles(img)
    return "User Delete"

@user.route("/users/getallusers", methods = ["GET"])
def getallusers(): #Temporal
    arrayProduct = []
    products = db.reference('/users').get()
    valuesProducts = products.values()
    keysProducts = products.keys()
    for key, value in products.items():
        value.setdefault("uid", key)
        arrayProduct.append(value)
    
    return flask.jsonify(arrayProduct)

@user.route("/users/getoneuser/<string:uidUser>", methods = ["GET"])
def getOneProduct(uidUser):
    user = db.reference('/users').child(uidUser).get()
    return flask.jsonify(user)

@user.route("/users/getoneuserbyname/<string:name>", methods = ["GET"])
def getOneUserByName(name):
    arr = []
    users = db.reference('/users').get()
    for key, value in users.items():
        if value['name'] == name:
            value.setdefault("uid", key)
            arr.append(value)

    return flask.jsonify(arr)