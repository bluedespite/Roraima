from flask import Flask,request,redirect,url_for
from flask import render_template,session

import secrets
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(20)

from datetime import datetime
from auth import *
from nodo import *
from init import *
from config import *
from graf import *

#Funciones Basicas de configuracion
user = { 'email':'','password':'','nombre':'','apellido':'','cargo':'','area':'','empresa':'','rol':''}
CONF = {'ID':'', 'ID_ESTACION': '','ESTACION': '', 'ID_TANQUE':'','TANQUE':'', 'PRODUCTO':'', 'DENSIDAD':'', 'TAG_SENSOR':'','DESCRIPCION':'','UM':'', 'RANGO_MIN':'', 'RANGO_MAX':'','TIPO':'','DIRECCION':'','MASCARA':'','PUERTO':'','ID_COMM':'','SERIAL':'','LINEAR':'','ENABLE':'' }
DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': '', 'MEDIDA':'', 'UM':'','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'', 'SALE':'', 'DELIVERY':'' }
CONX = { 'NOMBRE':'','DIRECCION':'','ENABLE':''}
     

#Tablas de Rutas
@app.route('/')
@app.route('/index')
def index():
    init_db()
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        if request.method=="POST":
            user={}
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            if val_user(user):
                session['username']=user['email']
                user = {}
                return render_template('dashboard.html')
            else:
                return redirect(url_for('index'))
        else:
                return redirect(url_for('index'))

@app.route('/saveconf', methods=["GET","POST"])
def saveconf():
    if request.method=="POST":
        CONF['ID_ESTACION']=request.form.get("ID_ESTACION")
        CONF['ESTACION']=request.form.get("ESTACION")
        CONF['ID_TANQUE']=request.form.get("ID_TANQUE")
        CONF['TANQUE']=request.form.get("TANQUE")
        CONF['PRODUCTO']=request.form.get("PRODUCTO")
        CONF['DENSIDAD']=request.form.get("DENSIDAD")
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        CONF['DESCRIPCION']=request.form.get("DESCRIPCION")
        CONF['UM']=request.form.get("UM")
        CONF['TIPO']=request.form.get("TIPO")
        CONF['RANGO_MIN']=request.form.get("RANGO_MIN")
        CONF['RANGO_MAX']=request.form.get("RANGO_MAX")
        CONF['DIRECCION']=request.form.get("DIRECCION")
        CONF['MASCARA']=request.form.get("MASCARA")
        CONF['PUERTO']=request.form.get("PUERTO")
        CONF['ID_COMM']=request.form.get("ID_COMM")
        CONF['SERIAL']=request.form.get("SERIAL")
        CONF['LINEAR']=request.form.get("LINEAR")       
        CONF['ENABLE']=request.form.get("ENABLE")
        return save_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/getconf', methods=["GET","POST"])
def getconf():
    if request.method=="POST":
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        return get_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/usuarios')
def usuarios():
    if 'username' in session:
        return render_template('usuarios.html')
    else:
        return redirect(url_for('index'))

@app.route('/configuracion')
def configuracion():
    if 'username' in session:
        return render_template('configuracion.html')
    else:
        return redirect(url_for('index'))

@app.route('/nodos')
def nodos():
    if 'username' in session:
        return render_template('nodos.html')
    else:
        return redirect(url_for('index'))

@app.route('/getuser', methods=["GET","POST"])
def getuser():
    if 'username' in session:
        if request.method=="POST":
            user['email']=request.form.get("email")
            return get_user(user)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/saveuser', methods=["GET","POST"])
def saveuser():
    if 'username' in session:
        if request.method=="POST":
            user['nombre']=request.form.get("nombre")
            user['apellido']=request.form.get("apellido")
            user['cargo']=request.form.get("cargo")
            user['rol']=request.form.get("rol")
            user['area']=request.form.get("area")
            user['empresa']=request.form.get("empresa")
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            user['npassword']=request.form.get("npassword")
            return save_user(user)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/getnodo', methods=["GET","POST"])
def getnodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            return get_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/savenodo', methods=["GET","POST"])
def savenodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            CONX['DIRECCION']=request.form.get("DIRECCION")
            CONX['ENABLE']=request.form.get("ENABLE")
            return save_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)



@app.route('/getchardata', methods=["GET","POST"])
def getchardata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_chartdata(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/getbardata', methods=["GET","POST"])
def getbardata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_bardata(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/getgeomapdata', methods=["GET","POST"])
def getgeomapdata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_geomap(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
