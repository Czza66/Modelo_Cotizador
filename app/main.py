from fastapi import FastAPI
from app.schemas import ProyectoRequest

from app.services.modelo_service import (
    entrenar_modelo,
    predecir
)

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import base64
import pandas as pd


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

class ArchivoRequest(BaseModel):
    filename: str
    content: str


@app.post("/cargar-excel")
def cargar_excel(request: ArchivoRequest):

    try:

        ruta_resources = Path("app/resources")
        ruta_resources.mkdir(parents=True, exist_ok=True)

        ruta_archivo = ruta_resources / "proyectos_entrenamiento.xlsx"

        archivo_bytes = base64.b64decode(request.content)

        with open(ruta_archivo, "wb") as f:
            f.write(archivo_bytes)

        df = pd.read_excel(ruta_archivo, engine="openpyxl")

        resultado_entrenamiento = entrenar_modelo()

        return {
            "success": True,
            "mensaje": "Archivo cargado correctamente",
            "filas": len(df),
            "resultado_entrenamiento": resultado_entrenamiento
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }