from flask import Blueprint,request
from V2.model import Conexion

solicitudBPV2=Blueprint('solicitudBPV2',__name__)

@solicitudBPV2.route('/Solicitudes/v2',methods=['POST'])
def agregarSolicitud():
    cn=Conexion()
    datos=request.get_json()
    return cn.insertar_solicitud(datos)