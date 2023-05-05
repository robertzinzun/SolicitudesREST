from flask import Blueprint,request
from V2.model import Conexion

solicitudBPV2=Blueprint('solicitudBPV2',__name__)

@solicitudBPV2.route('/Solicitudes/v2',methods=['POST'])
def agregarSolicitud():
    cn=Conexion()
    datos=request.get_json()
    return cn.insertar_solicitud(datos)

@solicitudBPV2.route('/Solicitudes/v2',methods=['GET'])
def consultaSolicitudes():
    cn=Conexion()
    return cn.consultaGeneralSolicitudes()

@solicitudBPV2.route('/Solicitudes/v2/<string:id>',methods=['GET'])
def consultarSolicitud(id):
    cn=Conexion()
    return cn.consultarSolicitud(id)