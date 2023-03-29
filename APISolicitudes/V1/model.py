from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String

db=SQLAlchemy()
class Opcion(db.Model):
    __tablename__='opciones'
    idOpcion=db.Column(Integer,primary_key=True)
    nombre=db.Column(String,nullable=False)
    descripcion=db.Column(String)
    estatus=db.Column(String,default='A')

    def consultaGeneral(self):#select * from opciones
        lista=self.query.all()
        respuesta={"estatus":"","mensaje":""}
        try:
            if len(lista)>0:
                respuesta["estatus"]="OK"
                respuesta["mensaje"]="Listado de opciones de titulacion."
                respuesta["opciones"]=[o.to_json() for o in lista]
            else:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "No hay opciones registradas"
                respuesta["opciones"]=[]
        except:
            respuesta["estatus"] = "Error"
            respuesta["mensaje"] = "Problemas de al ejecutar la consulta de opciones"
        return respuesta

    def to_json(self):
        o_json={"idOpcion":self.idOpcion,
                "nombre":self.nombre,
                "descripcion":self.descripcion
        }
        return o_json