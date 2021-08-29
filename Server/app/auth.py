import pymongo
from datetime import datetime
import bcrypt
import json

#Login de usuarios
def val_user(user):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "email": user['email'] }
    valor=db.USER.find_one(Query)
    hashed=valor['password']
    client.close()
    return bcrypt.checkpw(user['password'].encode('UTF-8'), hashed)

#Administracion de usuarios
def check_user(user):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "email": user['email'] }
    lon=db.USER.count_documents(Query)
    client.close()
    if lon>0:
        return True
    else:
        return False

def save_user(user):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    hashed = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
    user['password']=hashed
    Query={ "email": user['email'] }
    db.USER.update_one(Query,{"$set":user},upsert=True)
    client.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_user(user):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "email": user['email'] }
    resp=db.USER.find_one(Query)
    resp['_id']=''
    resp['password']=''
    message = {
        'status': 200,
        'message': 'OK',
        'data': resp
    }
    resp =  json.dumps(message, indent=4)
    return resp
