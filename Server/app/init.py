import pymongo
import bcrypt
import numpy as np
import random
from datetime import datetime, timedelta

#Inicializa las tablas necesarias dentro del dispositivo
def init_db():
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    password_inicial = "12345"
    hashed = bcrypt.hashpw(password_inicial.encode('utf-8'), bcrypt.gensalt())
    USER = { 'email':'miguelaguirreleon@gmail.com',
            'password':hashed,
            'nombre':'Miguel Angel',
            'apellido':'Aguirre Leon',
            'cargo':'Developer',
            'area':'DEV',
            'empresa':'DEV',
            'rol':'Administrador'}
    CONF = {'ID_ESTACION': 'EESS01',
            'ESTACION': 'Ciudad01', 
            'ID_TANQUE':'TK001',
            'TANQUE':'Tanque de Producto',
            'PRODUCTO':'Prodcuto01', 
            'DENSIDAD':750, 
            'TAG_SENSOR':'TEST001',
            'DESCRIPCION':'Nivel de Producto',
            'UM':'GAL', 
            'RANGO_MIN':0, 
            'RANGO_MAX':1000,
            'TIPO':'ANALOGICO',
            'DIRECCION':'192.168.1.20',
            'MASCARA':'255.255.255.0',
            'PUERTO': 520,
            'ID_COMM': 1,
            'REGISTRO':40020,
            'CANAL_AN':'AN0',
            'SERIAL': [9600,8,0,1],
            'LINEAR':[[0 ,50,100],[0, 50,100]],
            'ENABLE':True }
    DATA = { 'FECHA_HORA': '',
            'TAG_SENSOR': '', 
            'MEDIDA':'', 
            'UM':'',
            'VELOCIDAD':'',
            'LATITUD':'', 
            'LONGITUD':'', 
            'SALE':'', 
            'DELIVERY':'' }
    ARDUINO={'FECHA_HORA': datetime.now(),
            'LATITUD': 0, 
            'LONGITUD': 0, 
            'VELOCIDAD': 0, 
            'AN0': 0, 
            'AN1':0, 
            'AN2':0,
            'AN3':0, 
            'AN4':0}
    CONX = { 'NOMBRE':'CONEXION01',
            'DIRECCION':'mongodb://admin:12345@127.0.0.1:27017',
            'ENABLE':False}
    if db.USER.count_documents({})<1:
        db.USER.insert_one(USER)
        data=test()
        for elem in data:
            elem['_id']=db.DATA.count_documents({})
            db.DATA.insert_one(elem)
        for i in range(3):
            CONF['_id']=db.CONF.count_documents({})
            CONF['TAG_SENSOR']='TEST0'+str(i)
            db.CONF.insert_one(CONF)        
        client.close()

def test():
    POST=[]
    for i in range(3):
        f=1/100
        VANT=0
        for j in range(1000):
            DATA = {}
            DATA['TAG_SENSOR']='TEST0'+str(i)
            DATA['UM']='GAL'
            DATA['MEDIDA'] = 1200*np.sin(j*f+i*30)+random.random()/1000
            if DATA['MEDIDA']<0:
                DATA['MEDIDA']=0
            if DATA['MEDIDA']>1000:
                DATA['MEDIDA']=1000
            DATA['SALE']=0
            DATA['DELIVERY']=0
            if DATA['MEDIDA']-VANT>0.2:
                DATA['DELIVERY']=DATA['MEDIDA']-VANT
            if VANT-DATA['MEDIDA']>0.2:
                DATA['SALE']=VANT-DATA['MEDIDA']
            VANT=DATA['MEDIDA']
            DATA['LATITUD']= -12.063190+random.random()/100
            DATA['LONGITUD']= -77.112600+random.random()/100
            DATA['VELOCIDAD']= 100*random.random()
            DATA['FECHA_HORA']=datetime.now() - timedelta(minutes=(1000-j))
            POST.append(DATA)
    return POST

