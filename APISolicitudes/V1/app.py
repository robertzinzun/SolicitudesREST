from flask import Flask
from V1.model import Opcion,db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://titulatec_soa:Hola.123@localhost/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/',methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Solicitudes"

@app.route('/Solicitudes')
def listadoSolicitudes():
    respuesta={"estatus":"200","mensaje":"Listado de solicitudes"}
    return respuesta

@app.route('/Solicitudes/evidencias')
def listadoEvidencias():
    respuesta={"estatus":"200","mensaje":"Listado de evidencias de las solicitudes"}
    return respuesta
@app.route('/Solicitudes/<int:id>')
def eliminarSolicitud(id):
    respuesta={"estatus":"200","mensaje":"Eliminando la solicitud con id:"+str(id)}
    return respuesta

@app.route('/Solicitudes/<string:nc>')
def consultarSolicitud(nc):
    respuesta={"estatus":"200","mensaje":"Buscando la solicitud que registro el alumno con NC:"+nc}
    return respuesta

@app.route('/opciones',methods=['GET'])
def consultaOpciones():
    #retornar un listado de las opciones disponibles para titulación
    opcion=Opcion()
    print(opcion.consultaGeneral())
    return "Listado de opciones"


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)