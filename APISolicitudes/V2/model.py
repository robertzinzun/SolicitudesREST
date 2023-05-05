from pymongo import MongoClient
from datetime import date,timedelta
from bson import ObjectId

class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.titulaTEC
        self.coleccion=self.bd.solicitudes

    def insertar_solicitud(self,solicitud):
        resp={"estatus":"","mensaje":""}
        #Proceso de validación antes de registrar la solicitud
        alumno=self.bd.usuarios.find_one({"tipo":"E","alumno.idAlumno":solicitud["idAlumno"],"alumno.estatus":"E","estatus":"A"},projection={"alumno":True,"_id":False})
        if alumno:
            carrera=self.bd.carreras.find_one({"$and":[{"_id":alumno.get("alumno").get("carrera").get("idCarrera")},
                                              {"planesEstudio":{"$elemMatch":{"clave":alumno.get("alumno").
                                              get("carrera").get("plan"),"creditos":alumno.get("alumno").get("creditos")}}}]},
                                              projection={"jefePrograma":True,"_id":False})
            if carrera:
                count=self.coleccion.count_documents({"idAlumno":solicitud["idAlumno"],"estatus":{"$in":["Captura","Revision","Autorizada"]}})
                if count==0:
                    count=self.bd.opciones.count_documents({"_id":solicitud["idOpcion"],"estatus":True,
                                                            "carreras":{"$elemMatch":{"idCarrera":alumno.get("alumno").get("carrera").get("idCarrera"),
                                                            "planes":{"$in":[alumno.get("alumno").get("carrera").get("plan")]}}}})
                    if count>0:
                        solicitud["fechaRegistro"]=str(date.today())
                        sumaF=date.today()+timedelta(days=5)
                        solicitud["fechaAtencion"]=str(sumaF)
                        solicitud["estatus"]="Captura"
                        solicitud["idAdministrativo"]=carrera["jefePrograma"]
                        res=self.coleccion.insert_one(solicitud)
                        resp["estatus"] = "OK"
                        resp["mensaje"] = "Solicitud agregada con exito,con folio:"+str(res.inserted_id)
                    else:
                        resp["estatus"] = "Error"
                        resp["mensaje"] = "La opcion seleccionada no se encuentra vigente o no esta habilitada para el plan de estudios del alumno"
                else:
                    resp["estatus"] = "Error"
                    resp["mensaje"] = "El alumno ya tiene una solicitud en proceso o autorizada"
            else:
                resp["estatus"] = "Error"
                resp["mensaje"] = "El alumno no tiene los creditos suficientes de acuerdo a su plan de estudios"
        else:
            resp["estatus"] = "Error"
            resp["mensaje"] = "El alumno que intenta registrar la solicitud no existe o no es egresado"

        return resp

    def consultaGeneralSolicitudes(self):
        resp={"estatus":"","mensaje":""}
        res=self.bd.vSolicitudes2.find({})
        lista=[]
        for s in res:
            self.to_json_solicitud(s)
            lista.append(s)
        if len(lista)>0:
            resp["estatus"]="OK"
            resp["mensaje"]="listado de Solicitudes"
            resp["solicitudes"]=lista
        else:
            resp["estatus"] = "OK"
            resp["mensaje"] = "No hay Solicitudes registrado"
        return resp

    def to_json_solicitud(self,solicitud):
        solicitud["administrativo"]={"id":solicitud.get("administrativo")[0].get("id"),
                                     "nombre":solicitud.get("administrativo")[0].get("nombre")[0]}
        solicitud["alumno"]={"id":solicitud.get("alumno")[0].get("id"),
                             "NC":solicitud.get("alumno")[0].get("NC")[0],
                             "nombre":solicitud.get("alumno")[0].get("nombre")[0]}
        solicitud["carrera"]={"id":solicitud.get("carrera")[0].get("id")[0],
                              "nombre":solicitud.get("carrera")[0].get("nombre")[0]}
        solicitud["opcion"]={"id":solicitud.get("opcion")[0].get("id"),
                                     "nombre":solicitud.get("opcion")[0].get("nombre")[0]}
        solicitud["id"]=str(solicitud["id"])

    def consultarSolicitud(self,id):
        resp = {"estatus": "", "mensaje": ""}
        res = self.bd.vSolicitudes2.find_one({"id":ObjectId(id)})
        if res:
            self.to_json_solicitud(res)
            resp["estatus"] = "OK"
            resp["mensaje"] = "listado de la Solicitud"
            resp["solicitud"] = res
        else:
            resp["estatus"] = "OK"
            resp["mensaje"] = "No hay solicitudes registradas con ese id"
        return resp