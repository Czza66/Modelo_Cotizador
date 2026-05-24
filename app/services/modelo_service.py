import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

import matplotlib.pyplot as plt
import io
import base64

COLUMNAS_X = [
    "Dificultad",
    "Experticia",
    "ValorHora",
    "HorasEstimadas",
    "DuracionDias",
    "ClienteNuevo",
    "CambiosAlcance",
    "Retrasos"
]

COLUMNA_Y = "PrecioProyecto"

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "resources" / "proyectos_entrenamiento.xlsx"

modelo = None
error_promedio = 0
precision_modelo = 0


def entrenar_modelo():
    global modelo
    global error_promedio
    global precision_modelo

    df = pd.read_excel(EXCEL_PATH)

    df = df.dropna()

    X = df[COLUMNAS_X]
    y = df[COLUMNA_Y]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42
    )

    modelo = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    precision_modelo = r2_score(y_test, predicciones)
    error_promedio = mean_absolute_error(y_test, predicciones)

    # ================================
    # DIAGNÓSTICO DEL MODELO
    # ================================

    diagnostico = []
    recomendaciones = []

    cantidad_registros = len(df)

    # Cantidad de datos
    if cantidad_registros < 30:
        diagnostico.append("El modelo tiene muy pocos datos históricos.")
        recomendaciones.append("Agrega más proyectos al archivo Excel para que el modelo aprenda mejor.")
    elif cantidad_registros < 100:
        diagnostico.append("El modelo tiene una cantidad moderada de datos.")
        recomendaciones.append("Se recomienda aumentar la base histórica a más de 100 proyectos.")
    else:
        diagnostico.append("La cantidad de datos es adecuada para el entrenamiento.")

    # Precisión del modelo
    if precision_modelo < 0.50:
        diagnostico.append("La precisión del modelo es baja.")
        recomendaciones.append("Revisa si los precios históricos están bien calculados y si las columnas tienen datos coherentes.")
    elif precision_modelo < 0.80:
        diagnostico.append("La precisión del modelo es aceptable, pero puede mejorar.")
        recomendaciones.append("Agrega más variables como tipo de proyecto, tecnología usada, tamaño del equipo o urgencia del cliente.")
    else:
        diagnostico.append("El modelo tiene una buena capacidad de predicción.")

    # Importancia de variables
    importancias = modelo.feature_importances_

    variables_importancia = []

    for variable, importancia in zip(COLUMNAS_X, importancias):
        variables_importancia.append({
            "variable": variable,
            "importancia": round(float(importancia), 4)
        })

        if importancia < 0.05:
            recomendaciones.append(
                f"La variable '{variable}' tiene poca influencia. Revisa si realmente aporta valor al modelo."
            )

    # Variedad de datos por columna
    for columna in COLUMNAS_X:
        valores_unicos = df[columna].nunique()

        if valores_unicos <= 1:
            recomendaciones.append(
                f"La columna '{columna}' tiene muy poca variedad de datos. El modelo no puede aprender bien de esa variable."
            )

    return {
        "mensaje": "Modelo entrenado correctamente",
        "precision": round(precision_modelo, 2),
        "error_promedio": round(error_promedio, 2),
        "cantidad_registros": cantidad_registros,
        "diagnostico": diagnostico,
        "recomendaciones": recomendaciones,
        "importancia_variables": variables_importancia
    }

def generar_grafica_importancia():

    importancias = modelo.feature_importances_

    variables = COLUMNAS_X
    valores = importancias

    plt.figure(figsize=(10, 6))

    plt.barh(variables, valores)

    plt.title("Importancia de Variables")
    plt.xlabel("Nivel de importancia")
    plt.ylabel("Variables")

    plt.tight_layout()

    buffer = io.BytesIO()

    plt.savefig(buffer, format="png")

    plt.close()

    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


def generar_grafica_riesgo(
    precio_min,
    prediccion,
    precio_max,
    nivel_riesgo
):

    categorias = [
        "Mínimo",
        "Estimado",
        "Máximo"
    ]

    valores = [
        precio_min,
        prediccion,
        precio_max
    ]

    plt.figure(figsize=(8, 5))

    barras = plt.bar(categorias, valores)

    # Color según riesgo
    if nivel_riesgo == "Bajo":
        color = "green"
    elif nivel_riesgo == "Medio":
        color = "orange"
    else:
        color = "red"

    for barra in barras:
        barra.set_color(color)

    plt.title(
        f"Rango de Cotización - Riesgo {nivel_riesgo}"
    )

    plt.ylabel("Valor del proyecto")

    plt.tight_layout()

    buffer = io.BytesIO()

    plt.savefig(buffer, format="png")

    plt.close()

    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")



def predecir(data):

    global modelo

    if modelo is None:
        entrenar_modelo()

    nuevo = pd.DataFrame([{
        "Dificultad": data.dificultad,
        "Experticia": data.experticia,
        "ValorHora": data.valor_hora,
        "HorasEstimadas": data.horas_estimadas,
        "DuracionDias": data.duracion_dias,
        "ClienteNuevo": data.cliente_nuevo,
        "CambiosAlcance": data.cambios_alcance,
        "Retrasos": data.retrasos
    }])

    prediccion = modelo.predict(nuevo)[0]

    # ==========================
    # RANGO
    # ==========================

    precio_min = prediccion - error_promedio
    precio_max = prediccion + error_promedio

    if precio_min < 0:
        precio_min = 0

    # ==========================
    # RIESGO
    # ==========================

    puntaje_riesgo = (
        data.dificultad +
        data.cambios_alcance +
        data.retrasos +
        data.cliente_nuevo
    )

    if puntaje_riesgo <= 4:
        nivel_riesgo = "Bajo"

    elif puntaje_riesgo <= 7:
        nivel_riesgo = "Medio"

    else:
        nivel_riesgo = "Alto"

    # ==========================
    # GENERAR GRÁFICAS
    # ==========================

    grafica_importancia = generar_grafica_importancia()

    grafica_riesgo = generar_grafica_riesgo(
        precio_min,
        prediccion,
        precio_max,
        nivel_riesgo
    )

    # ==========================
    # RESPUESTA
    # ==========================

    return {

        "precio_estimado": round(prediccion, 2),

        "rango_sugerido": {
            "desde": round(precio_min, 2),
            "hasta": round(precio_max, 2)
        },

        "nivel_riesgo": nivel_riesgo,

        "precision_modelo": round(
            precision_modelo,
            2
        ),

        "error_promedio": round(
            error_promedio,
            2
        ),

        "graficas": {

            "grafica_importancia_variables":
                grafica_importancia,

            "grafica_riesgo_rango":
                grafica_riesgo
        }
    }