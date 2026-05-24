from fastapi import FastAPI
from app.schemas import ProyectoRequest

from app.services.modelo_service import (
    entrenar_modelo,
    predecir
)

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

app = FastAPI()


@app.get("/")
def home():
    return {
        "mensaje": "API IA funcionando correctamente"
    }


@app.post("/entrenar")
def entrenar():
    return entrenar_modelo()


@app.post("/predecir")
def prediccion(data: ProyectoRequest):
    return predecir(data)


@app.post("/cargar-excel")
def cargar_excel(file: UploadFile = File(...)):

    if not file.filename.endswith(".xlsx"):
        return {
            "error": "Solo se permiten archivos Excel con extensión .xlsx"
        }

    ruta_resources = Path("app/resources")
    ruta_resources.mkdir(parents=True, exist_ok=True)

    ruta_archivo = ruta_resources / "proyectos_entrenamiento.xlsx"

    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resultado_entrenamiento = entrenar_modelo()

    return {
        "mensaje": "Archivo cargado y modelo entrenado correctamente",
        "archivo_guardado": "proyectos_entrenamiento.xlsx",
        "resultado_entrenamiento": resultado_entrenamiento
    }