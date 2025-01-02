#API REST: interfaz de progracion de aplicaciones para compartir recursos (buscar info mas precisa)

from tkinter import N
from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#incializamos una variable con las caracteristica de una API REST
app = FastAPI()

#Aca definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#Simularemos una base de datos
cursos_db = []

#CRUD: READ (lectura) GET ALL: leeremos todos los cursos que hay en la base de datos

@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return cursos_db

#CRUD: CREATE (CREAR) POST: se añade recursos a la base de datos

@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) #USAMOS UUID para generar un id unico
    cursos_db.append(curso)
    return curso

#CRUD: READ (lectura) GET: leeremos un recurso individual

@app.get("/curso/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con next se toma la primer coincidencia en el array
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrad")
    return curso

#CRUD: UPDATE (actualizarU/modificar) PUT: modificamos un recurso que coincida con el ID que mandamos

@app.put("/curso/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con next se toma la primer coincidencia en el array
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrad")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) #buscamos el indice del curso a modificar
    cursos_db[index]
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#CRUD: DELETE (eliminar) DELETE: se eliminar el recurso que coincida con el id que mandamos
@app.delete("/curso/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con next se toma la primer coincidencia en el array
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrad")
    cursos_db.remove(curso)
    return curso