import pymongo
from datetime import datetime
import bcrypt
import json

#Login de usuarios
def check_nodo(CONX):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "NOMBRE": CONX['NOMBRE'] }
    lon=db.CONX.count_documents(Query)
    client.close()
    if lon>0:
        return True
    else:
        return False

def save_nodo(CONX):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "NOMBRE": CONX['NOMBRE'] }
    db.CONX.update_one(Query,{"$set":CONX},upsert=True)
    client.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_nodo(CONX):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "NOMBRE": CONX['NOMBRE'] }
    resp=db.CONX.find_one(Query)
    resp['_id']=''
    message = {
        'status': 200,
        'message': 'OK',
        'data': resp
    }
    resp =  json.dumps(message, indent=4)
    return resp

