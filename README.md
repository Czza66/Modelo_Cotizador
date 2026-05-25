# Sistema de Predicción Inteligente de Precios de Proyectos

## Descripción general del proyecto

Este proyecto consiste en una API desarrollada con Python y Machine Learning capaz de estimar automáticamente el valor aproximado de un proyecto tecnológico a partir de diferentes variables como dificultad, horas estimadas, experiencia requerida, valor por hora y posibles riesgos del proyecto.

La idea principal fue construir una solución inteligente que ayudara a mejorar el proceso de cotización de proyectos, ya que normalmente estas estimaciones se realizan manualmente y pueden variar mucho dependiendo de la experiencia de cada persona.

---

# Problema o necesidad que se quiso solucionar mediante IA

En muchas empresas tecnológicas las cotizaciones de proyectos se realizan de forma manual, basándose únicamente en experiencia humana o aproximaciones subjetivas. Esto puede generar:

- Cotizaciones incorrectas
- Pérdidas económicas
- Mala rentabilidad
- Subestimación de horas
- Sobre costos
- Riesgos no contemplados

Por esta razón se desarrolló una solución basada en Inteligencia Artificial capaz de aprender de proyectos históricos y generar predicciones automáticas más precisas.

---

# Librerías, frameworks y recursos utilizados

## Backend

- FastAPI
- Python 3.13

## Librerías de Machine Learning

- pandas
- scikit-learn
- matplotlib
- openpyxl
- numpy

## Recursos utilizados

- Dataset histórico en Excel
- Swagger UI para pruebas de API
- Visual Studio Code
- FastAPI Docs

---

# Cómo se construyó el dataset

El dataset fue construido manualmente utilizando información histórica simulada de proyectos tecnológicos.

Cada fila del Excel representa un proyecto distinto y contiene variables relacionadas con:

- Dificultad del proyecto
- Nivel de experiencia requerido
- Valor por hora
- Horas estimadas
- Duración en días
- Riesgo de retrasos
- Cambios de alcance
- Si el cliente es nuevo
- Precio final del proyecto

Toda esta información fue organizada en un archivo Excel utilizado posteriormente para entrenar el modelo.

---

# Cantidad de entradas utilizadas para entrenar el modelo

El modelo fue entrenado inicialmente con múltiples registros históricos almacenados en un archivo Excel dinámico.

La solución fue diseñada para permitir que el dataset pueda crecer con el tiempo mediante carga de nuevos archivos Excel desde la API.

---

# Modelos de Machine Learning utilizados

Se utilizó principalmente el modelo:

- Random Forest Regressor

---

# ¿Por qué se eligió este modelo?

Se eligió Random Forest porque:

- Tiene muy buen rendimiento en predicciones numéricas
- Maneja muy bien relaciones complejas entre variables
- Reduce el riesgo de sobreajuste
- Funciona correctamente incluso con datasets pequeños o medianos
- Permite analizar importancia de variables
- Tiene buena precisión sin requerir configuraciones demasiado complejas

Además, fue uno de los modelos que entregó mejores resultados durante las pruebas iniciales.

---

# Nivel de efectividad o métricas obtenidas

Durante las pruebas se utilizaron métricas como:

## Precisión R²

Permite medir qué tan bien el modelo logra entender el comportamiento de los datos.

## Error promedio (MAE)

Permite medir aproximadamente cuánto dinero puede variar la predicción respecto al valor real.

El modelo logró resultados bastante positivos para el tamaño del dataset utilizado.

---

# Predicciones generadas por el sistema

El sistema es capaz de generar automáticamente:

- Precio estimado del proyecto
- Rango mínimo y máximo sugerido
- Nivel de riesgo del proyecto
- Importancia de variables
- Recomendaciones automáticas para mejorar precisión
- Diagnóstico del modelo
- Gráficas dinámicas en Base64

---

# Cómo las predicciones fueron utilizadas para construir una solución de cara al usuario

Las predicciones fueron utilizadas para construir una API inteligente orientada a ayudar en procesos de cotización.

La API no solo entrega un valor numérico, sino también:

- Explicaciones visuales
- Gráficas automáticas
- Riesgo del proyecto
- Variables más importantes
- Recomendaciones comerciales

Esto permite que el usuario final pueda entender mejor el resultado generado por la IA.

---

# Cómo se llevó la solución a la web

La solución fue desarrollada mediante una API REST utilizando FastAPI.

La API expone endpoints como:

- `/predecir`
- `/entrenar`
- `/cargar-excel`

Adicionalmente se utilizó Swagger UI para visualizar y probar los servicios web directamente desde el navegador.

---

# Explicación general del frontend y backend

## Backend

El backend fue desarrollado completamente en Python utilizando FastAPI.

El sistema se encarga de:

- Recibir datos
- Entrenar modelos
- Procesar predicciones
- Generar gráficas
- Analizar métricas
- Retornar respuestas JSON

## Frontend

La solución utiliza Swagger UI como interfaz inicial de pruebas.

Sin embargo, la API fue diseñada para poder conectarse posteriormente a:

- power apps
- power automate

---

# Cómo se aprovecharon las predicciones para generar nuevas reglas o comportamientos

Las predicciones no solo se utilizaron para mostrar precios, sino también para generar reglas automáticas dentro del sistema.

Por ejemplo:

- Detectar proyectos de alto riesgo
- Recomendar aumentar márgenes de cotización
- Identificar variables poco útiles
- Alertar cuando el dataset tiene pocos datos
- Recomendar mejoras para aumentar precisión

Esto permitió convertir la IA en una herramienta de apoyo para toma de decisiones.

---

# Cómo funciona la interfaz final y cuál es su objetivo

La interfaz principal funciona mediante Power Apps.

El usuario puede:

1. Cargar un archivo Excel
2. Entrenar el modelo automáticamente
3. Realizar predicciones
4. Visualizar resultados
5. Obtener gráficas generadas por IA

El objetivo principal del sistema es ayudar a mejorar los procesos de cotización y análisis financiero de proyectos tecnológicos mediante Inteligencia Artificial.

---

# Ejecución del proyecto

## Crear entorno virtual

```bash
py -m venv venv
```

## Activar entorno virtual

```bash
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar API

```bash
uvicorn app.main:app --reload
```

## Abrir Swagger

```text
https://modelo-cotizador.onrender.com/docs#/
```

---

# Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Verificar funcionamiento API |
| POST | `/predecir` | Generar predicción |
| POST | `/cargar-excel` | Cargar nuevo dataset |

---

# Video en Youtube
https://youtu.be/d_wluzNgsz4

# AUTOR
Desarrollador por Juan Sebastian Briñez Capera, Ingenieria de Software en UComepensar
