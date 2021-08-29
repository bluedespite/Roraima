import pymongo
from datetime import datetime
import json



#Datos para graficas entre fecha_inicio y fecha_fin
def Queryalldatos(fecha_inicio,fecha_fin):
    f=open('database.env')
    client = pymongo.MongoClient(f.read())
    f.close()
    db=client.MAIN_SERVER
    labels=[]
    data=[]
    Query={ "FECHA_HORA": { '$gte': fecha_inicio, '$lte': fecha_fin }}
    dd={}
    for elem in db.DATA.aggregate(pipeline=[{'$match':Query},{'$group': {'_id':'$TAG_SENSOR','um':{'$last':'$UM'},'sale':{'$sum':'$SALE'}, 'delivery':{'$sum':'$DELIVERY'}}}]):
        dd[elem['_id']]={'UM':elem['um'],'SALE':elem['sale'],'DELIVERY':elem['delivery']}
    print(dd)
    for tag in db.CONF.find().distinct('TAG_SENSOR'):
        labels.append(tag)
        Query={ "FECHA_HORA": { '$gte': fecha_inicio, '$lte': fecha_fin }, 'TAG_SENSOR':{'$eq':tag}}
        q0=[]
        q1=[]
        for d in db.DATA.find(Query):
            q0.append({'t':d['FECHA_HORA'].strftime('%Y-%m-%dT%H:%M:%S'),'y':d['MEDIDA']})
            q1.append({'lat':d['LATITUD'],'lon':d['LONGITUD']})
        data.append({
            'DATA':q0,
            'TAG_SENSOR': tag,
            'UM': dd[tag]['UM'],
            'SALES':dd[tag]['SALE'],
            'DELIVERY': dd[tag]['DELIVERY'],
            'GEO':q1
        })
    client.close
    return labels,data

def get_chartdata(fecha_inicio,fecha_fin):
    import random
    print(fecha_inicio)
    labels,datos=Queryalldatos(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'),datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))
    datasets=[]
    chartdata={}
    for i in range(len(datos)):
        color=str(255*random.random())+','+str(255*random.random())+','+str(255*random.random())
        datasets.append({
            'label': labels[i],
            'data': datos[i]['DATA'],
            'lineTension': '0',
            'backgroundColor': 'rgba('+color+',0.2)',
            'borderColor': 'rgba('+color+',1)'})
    chartdata={'labels':labels, 'datasets': datasets}
    message = {
            'status': 200,
            'message': 'OK',
            'data': chartdata
        }
    resp =  json.dumps(message, indent=4)
    return resp

def Querybardata(fecha_inicio,fecha_fin):
    labels,datos=Queryalldatos(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'),datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))    
    sales=[]
    deliveries=[]
    for i in range(len(datos)):
        sales.append(datos[i]['SALES'])
        deliveries.append(datos[i]['DELIVERY'])
    data={
        'labels': labels,
        'datasets': [
        {'label': "Sales",
          'backgroundColor': "#3e95cd",
          'data': sales
        }, {
          'label': "Deliveries",
          'backgroundColor': "#8e5ea2",
          'data': deliveries
        }]}
    return data


def get_bardata(fecha_inicio,fecha_fin):
    datos=Querybardata(fecha_inicio,fecha_fin)
    message = {
            'status': 200,
            'message': 'OK',
            'data': datos
        }
    resp =  json.dumps(message, indent=4)
    return resp

#Datos para graficas entre fecha_inicio y fecha_fin
def Querygeodatos(fecha_inicio,fecha_fin):
    labels,datos=Queryalldatos(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'),datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))    
    geo=[]
    gdata=[]
    for i in range(len(datos)):
        for g in datos[i]['GEO']:
            geo.append([g['lat'],g['lon']])
        gdata.append({
            'TAG_SENSOR': datos[i]['TAG_SENSOR'],
            'GEO':geo
        })
    return gdata

def get_geomap(fecha_inicio,fecha_fin):
    gdata=Querygeodatos(fecha_inicio,fecha_fin)    
    message = {
            'status': 200,
            'message': 'OK',
            'data':gdata
        }
    resp =  json.dumps(message, indent=4)
    return resp
