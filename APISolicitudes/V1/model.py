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
        return lista