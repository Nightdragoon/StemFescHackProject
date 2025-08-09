<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
=======
from fastapi import FastAPI
import json
>>>>>>> d8cdefcefd3e2d00db6dfc26baaee1e4bcf279f7
from ChatGptEntranceDto import ChatGptEntranceDto
from ChatGptConexion import ChatGptConexion
from LessonDto import HybridLesson

app = FastAPI()

print("--- MAIN.PY HA SIDO CARGADO ---")
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/chatGptConexion")
async def connect(entrance: ChatGptEntranceDto):
    conexion = ChatGptConexion()
    mensaje = entrance.message
    return await conexion.conectar(mensaje)

<<<<<<< HEAD
# --- 2. NUEVO ENDPOINT PARA GENERAR GUIONES ---
@app.post("/create-hybrid-lesson-plan/", response_model=HybridLesson)
async def create_hybrid_lesson_plan(topic: str):
    """
    Genera un plan de lección estructurado para un videotutorial híbrido.
    """
    # Creamos un prompt de sistema muy específico para guiar a la IA
    system_prompt = f"""
    Eres un guionista experto para tutoriales de IA en YouTube.
    Tu tarea es crear el guion para un video de 5 minutos sobre el tema: "{topic}".
    El video tiene un formato Híbrido: primero explica la teoría y luego muestra cómo aplicarla con código.
    Debes devolver tu respuesta exclusivamente en formato JSON, siguiendo esta estructura exacta:
=======


@app.post("/human")
async def human(entrance: HumanEntrance):
    mensaje = entrance.message
    humanAi = HumanEntrance()
    conexion = humanAi.conectar(mensaje)
    jsonstring = json.loads(conexion)
    root = HumanDto.from_dict(jsonstring)
>>>>>>> d8cdefcefd3e2d00db6dfc26baaee1e4bcf279f7

    {{
      "title": "string",
      "theory_script": "string",
      "bridge_script": "string",
      "tooling_script_steps": ["string", "string", "..."]
    }}
    """

    try:
        # Usamos tu clase de conexión existente
        conexion = ChatGptConexion()
        # Llamamos a tu método 'conectar' con el prompt detallado
        response_from_api = await conexion.conectar(system_prompt)

        # La respuesta de la API puede venir como un string o ya como un diccionario.
        # Nos aseguramos de que sea un diccionario para poder trabajarlo.
        if isinstance(response_from_api, str):
            # Si es un string, lo parseamos a JSON (diccionario)
            lesson_data = json.loads(response_from_api)
        else:
            # Si ya es un diccionario, lo usamos directamente
            lesson_data = response_from_api
        
        # Pydantic usa el diccionario para crear y validar nuestro objeto HybridLesson
        lesson_plan = HybridLesson(**lesson_data)
        
        return lesson_plan

    except Exception as e:
        # Manejo de errores por si la API falla o el JSON es inválido
        raise HTTPException(status_code=500, detail=f"Error al generar el plan de lección: {str(e)}")

