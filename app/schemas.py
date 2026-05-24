from pydantic import BaseModel

class ProyectoRequest(BaseModel):
    dificultad: int
    experticia: int
    valor_hora: float
    horas_estimadas: float
    duracion_dias: int
    cliente_nuevo: int
    cambios_alcance: int
    retrasos: int