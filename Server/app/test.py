from datetime import datetime, timedelta
import random
import numpy as np
import pymongo

prct=0.005 #0.5% de cambios
f=open("database.env")
dbc = urlparse(f.read())
f.close()
def sin_wave():
    for i in range(3):
        connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
        cursor=connection.cursor()
        TOT_D=0
        TOT_S=0
        D=[]
        y=[]
        x=[]
        f=1/100
        VANT=0
        DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': 'TEST0'+str(i), 'MEDIDA':'', 'UM':'GAL','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'', 'SALE':'', 'DELIVERY':'' }
        for x1 in range(0,1000):
            DATA['MEDIDA'] = 1200*np.sin(x1*f+i*30)+random.random()/1000
            if DATA['MEDIDA']<0:
                DATA['MEDIDA']=0
            if DATA['MEDIDA']>1000:
                DATA['MEDIDA']=1000
            DATA['SALE']=0
            DATA['DELIVERY']=0
            if DATA['MEDIDA']-VANT>0.2:
                DATA['DELIVERY']=DATA['MEDIDA']-VANT
                TOT_D+=DATA['DELIVERY']
            if VANT-DATA['MEDIDA']>0.2:
                DATA['SALE']=VANT-DATA['MEDIDA']
                TOT_S+=DATA['SALE']
            VANT=DATA['MEDIDA']
            y.append(DATA['MEDIDA'])
            x.append(x1)
            DATA['LATITUD']= -12.063190+random.random()/1000
            DATA['LONGITUD']= -77.112600+random.random()/1000
            DATA['VELOCIDAD']= 100*random.random()
            tiempo=datetime.now() - timedelta(minutes=1000-x1)
            DATA['FECHA_HORA']=tiempo.strftime('%Y-%m-%d %H:%M:%S')
            D.append(DATA)
            Query='INSERT INTO DATA (FECHA_HORA, TAG_SENSOR,MEDIDA,UM,VELOCIDAD,LATITUD,LONGITUD, SALE,DELIVERY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(Query,(DATA['FECHA_HORA'],DATA['TAG_SENSOR'],DATA['MEDIDA'],DATA['UM'], DATA['VELOCIDAD'],DATA['LATITUD'],DATA['LONGITUD'],DATA['SALE'],DATA['DELIVERY']))
        connection.commit()
        cursor.close()
        connection.close()
        print('insertado tag'+str(i))
    return 'exito'

msj=sin_wave()
print(msj)

