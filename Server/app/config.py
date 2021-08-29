import pymongo
from datetime import datetime
import json

def check_conf(CONF):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "TAG_SENSOR": CONF['TAG_SENSOR'] }
    lon=db.CONF.count_documents(Query)
    client.close()
    if lon>0:
        return True
    else:
        return False

def save_conf(CONF):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "TAG_SENSOR": CONF['TAG_SENSOR'] }
    db.CONF.update_one(Query,{"$set":CONF},upsert=True)
    client.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_conf(CONF):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    Query={ "TAG_SENSOR": CONF['TAG_SENSOR'] }
    resp=db.CONF.find_one(Query)
    resp['_id']=''
    message = {
        'status': 200,
        'message': 'OK',
        'data': resp
    }
    resp =  json.dumps(message, indent=4)
    return resp


