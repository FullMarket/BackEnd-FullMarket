from itertools import product
import flask
import firebase_admin
from firebase_admin import auth, db
import cloudinary
import cloudinary.uploader
import urllib.parse
import hashlib

products = flask.Blueprint('products', __name__)

def UploadFiles(file, uidOwner, filename): 
    LoadFile = cloudinary.uploader.upload(file, folder = f"products/{uidOwner}", public_id = filename)
    return LoadFile['url']

def DeleteOrPutFiles(publicid):
    Delete = cloudinary.uploader.destroy(publicid)
    return Delete

@products.route("/products/createnewproduct", methods = ["POST"])
def createNewProduct():
    name = flask.request.form.get('name')
    imgProduct = flask.request.files.get('imgProduct')
    date = flask.request.form.get('date')
    description = flask.request.form.get('description')
    condition = flask.request.form.get('condition')
    availability = flask.request.form.get('availability') 
    category =  flask.request.form.get('category')
    city = flask.request.form.get('city')
    type = flask.request.form.get('type')
    idOwner = flask.request.form.get('idOwner')

    if not availability:
        availability = 'Si'
    
    if not condition:
        condition = 'Usado'

    imgProductURL = UploadFiles(imgProduct, idOwner ,imgProduct.filename)
    producToDB = db.reference('/products').push({
        'name': name,
        'imgProductURL': imgProductURL,
        'date': date,
        'description': description,
        'condition': condition,
        'availability': availability,
        'category': category,
        'city': city,
        'type': type,
        'idOwner': idOwner
    })
    return "Product Create"

@products.route("/products/editproduct/<string:uidProduct>", methods = ["PUT"])
def editNProduct(uidProduct):
    product = {
        'name': flask.request.form.get('name'),
        # 'imgProduct': flask.request.files.get('imgProduct'),
        'date': flask.request.form.get('date'),
        'description': flask.request.form.get('description'),
        'condition': flask.request.form.get('condition'),
        'availability': flask.request.form.get('availability'), 
        'city': flask.request.form.get('city'),
        'type': flask.request.form.get('type'),
    }
    getProduct = db.reference('/products').child(uidProduct).update(product)
    return "Product Updated"


@products.route("/products/deleteproduct/<string:uidProduct>", methods = ["DELETE"])
def deleteProducstN(uidProduct):
    urlimg = db.reference('/products').child(uidProduct).get()['imgProductURL']
    urlimgDecode = urllib.parse.unquote(urlimg)
    db.reference('/products').child(uidProduct).set({})
    positionfile = urlimgDecode.find('products')
    img = urlimgDecode[positionfile: -4]
    imgDelete = DeleteOrPutFiles(img)

    return "Product Delete"

@products.route('/products/getallproducts', methods = ["GET"])
def getAProduct():
    array = []
    prod = db.reference('/products').get()
    for key, value in prod.items():
        if value['availability'] == 'Si':
            value.setdefault("uid", key)
            array.append(value)

    return flask.jsonify(array)

@products.route("/products/getoneproduct/<string:uidProduct>", methods = ["GET"])
def getOneProduct(uidProduct):
    produc = db.reference('/products').child(uidProduct).get()
    oneproduct = produc|{'uidProduct': uidProduct}

    return flask.jsonify(oneproduct)

@products.route("/products/getmyproducts/<string:uidUser>", methods=["GET"])
def getMyProducts(uidUser): 
    arrayProducts = []
    products = db.reference('/products').get()
    for key, value in products.items(): 
        if value['idOwner'] == uidUser:
            value.setdefault("uidProduct", key)
            arrayProducts.append(value)

    return flask.jsonify(arrayProducts)

@products.route("/products/productsbycategory/<string:categoryProduct>", methods = ["GET"])
def getAProductByCategory(categoryProduct):
    arrayP = []
    prodr = db.reference('/products').get()
    for key, value in prodr.items():
        if value['availability'] == 'Si' or 'SI' or 'si' or 'sI':
            if value['category'] == categoryProduct:
                value.setdefault("uid", key)
                arrayP.append(value)

    return flask.jsonify(arrayP)

@products.route("/products/getproductbyname/<string:nameProduct>", methods = ["GET"])
def getProductByName(nameProduct):
    arrayP = []
    prodch = db.reference('/products').get()
    for key, value in prodch.items():
        if value['name'] == nameProduct:
            value.setdefault("uid", key)
            arrayP.append(value)

    return flask.jsonify(arrayP)

@products.route("/products/putproducttonotavaible/<string:nameProduct>", methods = ["PUT"])
def putProductNotAvaible(nameProduct):
    arr = []
    getPrd = db.reference('/products').get()
    for key, value in getPrd.items():
        if value['name'] == nameProduct:
            db.reference('/products').child(key).update({'availability': 'No'})

    return flask.jsonify('Update')