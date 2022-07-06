import firebase_admin
from firebase_admin import db
import flask
import decouple

noti = flask.Blueprint('noti', __name__)

@noti.route("/notification/sendnotification", methods = ["POST"])
def newuseronline(): 
  userSendNoti = flask.request.form.get('usersendnoti')
  userReceiverNoti = flask.request.form.get('userreceivernoti')
  userReceiverNotiProduct = flask.request.form.get('userreceivernotiproduct')
  typeNoti = flask.request.form.get('typenoti')
  sendUsersOnline = db.reference('/notifications').push({
    'userSendNoti': userSendNoti,
    'userReceiverNoti': userReceiverNoti,
    'userReceiverNotiProduct': userReceiverNotiProduct,
    'typeNoti': typeNoti
  })
  return 'Notification Send'
 
@noti.route("/notification/getnotificationuser/<string:uidUser>",  methods=["GET"])
def getusernotification(uidUser):
  notificationUser = []
  notification = db.reference('/notifications').get()
  for key, value in notification.items():
    if value['userReceiverNoti'] == uidUser:
      value.setdefault("UIDNoti", key)
      notificationUser.append(value)
  
  return flask.jsonify(notificationUser)
  
@noti.route("/notification/deleteNotification/<string:uidNoti>", methods = ["DELETE"])
def DeleteNotification(uidNoti):
  db.reference('/notifications').child(uidNoti).set({})
  return "Notification Delete"