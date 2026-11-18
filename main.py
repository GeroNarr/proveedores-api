from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cliente = MongoClient(os.environ.get("MONGO_URI"))
db = cliente["ISIS2304E06202620"]

@app.get("/")
def inicio():
    return {"Estado": "API funcionando correctamente"}

@app.get('/proveedores')
def get_proveedores():
    proveedores = list(db.proveedores.find({}, {"_id": 0}))
    return proveedores

@app.get("/proveedores/{bebida_id}")
def get_proveedor(bebida_id: int):
    proveedor = db.proveedores.find_one({"bebidas_suministradas": bebida_id},
                                        {"_id": 0})
    return proveedor or {}

@app.post('/proveedores')
def post_proveedor(datos: dict):
    datos['fecha_registro'] = datetime.now().isoformat()
    db["proveedores"].insert_one(datos)
    return {'mensaje': 'Proveedor registrado'}



@app.put('/proveedores/{nombre}')
def put_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].replace_one({"nombre": nombre}, {"$set": datos})
    return {"mensaje": "Proveedor actualizado"}

@app.patch('/proveedores/{nombre}')
def patch_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].update_one({"nombre": nombre}, {"$set": datos})
    return {"mensaje": "Campos actualizados correctamente"}

@app.delete('/proveedores/{nombre}')
def delete_proveedor(nombre: str):
    resultado = db["proveedores"].delete_one({"nombre": nombre})
    return {"mensaje": "Proveedor {nombre} eliminado"}


