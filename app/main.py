import logging
import pymongo
import time
import bcrypt
import serial
import serial.tools.list_ports
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient


def init_db(db):
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
        db.DATA.insert_one(DATA)
        db.ARDUINO.insert_one(ARDUINO)
        db.CONX.insert_one(CONX)
        db.CONF.insert_one(CONF)


def init_logger():
    FORMAT = ('%(asctime)s - %(threadName)s %(levelname)s %(module)s %(lineno)s %(message)s')
    logging.basicConfig(filename='Roraima_Log.txt', filemode='w',format=FORMAT)
    log=logging.getLogger()
    log.setLevel(logging.DEBUG)

def init_arduino():   
    arduino_ports=[]
    for p in serial.tools.list_ports.comports():
        if 'Arduino' in p.manufacturer:
            arduino_ports = p.device
            logging.info("Info Puerto Serie Arduino:"+str(p.device))
            return arduino_ports,True
    return arduino_ports,False

def Arduino_Comm(db):
    ARDUINO={}
    arduino_port,OK = init_arduino()
    arduino = serial.Serial(arduino_port,9600, timeout=50)
    time.sleep(10)
    if OK:
        comando = 'GO!'+'\n'
        a=arduino.write(comando.encode())
        lectura = arduino.readline() 
        txt=str(lectura)
        txt=txt[2:-5]
        print(txt)
        if txt.find('LATITUD')<0  or txt.find('LONGITUD')<0:
            logging.info("Error de lectura en cadena Serial")
        else:
            SerialA=txt.split("|")
            for S in SerialA:
                CLAVE=S.split("=")[0]
                VALOR=S.split("=")[1]
                if VALOR=="INVALID DATETIME":
                    VALOR=datetime.now()
                if VALOR=="INVALID SPEED":
                    VALOR=0
                if VALOR=="INVALID LATITUDE":
                    VALOR=0
                if VALOR=="INVALID LONGITUDE":
                    VALOR=0
                if CLAVE=='FECHA_HORA':
                    ARDUINO[CLAVE]=datetime.now()
                else:
                    ARDUINO[CLAVE]=float(VALOR)
            db.ARDUINO.insert_one(ARDUINO)
    else:
        logging.error("No se puede contectar a Tarjeta ARDUINO") 

def Read_Conf(db):
    CONFIG=[]
    for post in db.CONF.find():
        CONFIG.append(post)
    return CONFIG


def linealization(valor,tabla):
    for i in range(len(tabla)-1):
        x1=tabla[0][i]
        y1=tabla[1][i]
        x2=tabla[0][i+1]
        y2=tabla[1][i+1]
        if (valor>=x1 and valor<=x2):
            try:
                valor=(valor-x1)*((y2-y1)/(x2-x1))+y1
                return valor
            except:
                return 0
    return valor

def Read_Measure(db,CONFIG):
    t=[T for T in db.ARDUINO.find().sort([('$natural',-1)])]
    ARDUINO=t[0]
    for i in range(len(CONFIG)):
        Med_lin=0
        if CONFIG[i]['TIPO']=='MODBUS_TCP':
            client = ModbusTcpClient(CONFIG[i]['DIRECCION'],port=int(CONFIG[i]['PUERTO']))
            if client.connect():
                ID=CONFIG[i]['ID']
                DIRECCION=CONFIG[i]['REGISTRO']-40001
                try:
                    rr = client.read_holding_registers(DIRECCION,1,unit=ID)
                    Med_lin=linealization(rr.registers[0],CONFIG[i]['LINEAR'])
                except:
                    logging.exception("No se puede leer registros: "+ CONFIG[i]['TAG_SENSOR'])
        if CONFIG[i]['TIPO']=="ANALOGICO":
            canal=CONFIG[i]['CANAL_AN']
            try:
                rANA=(ARDUINO[canal]-(1024/5))/(1024-(1024/5))
                rMed=rANA*(CONFIG[i]['RANGO_MAX']-CONFIG[i]['RANGO_MIN'])+CONFIG[i]['RANGO_MIN']
                Med_lin=linealization(rMed,CONFIG[i]['LINEAR'])
            except:
                logging.error("Error en sensor Analogico: " + CONFIG[i]['TAG_SENSOR'])
        DATA = { 'FECHA_HORA': datetime.now(),
                                'TAG_SENSOR': CONFIG[i]['TAG_SENSOR'], 
                                'MEDIDA': Med_lin, 
                                'UM': CONFIG[i]['UM'],
                                'VELOCIDAD':ARDUINO['VELOCIDAD'],
                                'LATITUD':ARDUINO['LATITUD'], 
                                'LONGITUD':ARDUINO['LONGITUD'], 
                                'SALE':'', 
                                'DELIVERY':'' }
        db.DATA.insert_one(DATA)
        
init_logger()
f=open('database.env')
client = pymongo.MongoClient(f.read())
f.close()
db=client.MAIN_SENSOR
init_db(db)

if True:
    Arduino_Comm(db)
    if db.CONF.count_documents({})>0:
        CONFIG=Read_Conf(db)
        Read_Measure(db,CONFIG)
    time.sleep(10)