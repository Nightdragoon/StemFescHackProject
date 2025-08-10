
from fastapi import FastAPI, HTTPException
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
import json
import uuid
from ChatGptEntranceDto import ChatGptEntranceDto
from ChatGptConexion import ChatGptConexion
from HumanEntrance import HumanEntrance
from LessonDto import HybridLesson
from HumanAiConexion import HumanAiConexion
from EmotionEntrance import EmotionEntrance
from EmotionConexion import EmotionConexion
from sqlalchemy import create_engine , String
from sqlalchemy.orm import sessionmaker, declarative_base,Mapped, mapped_column
from RegisterEnter import RegisterEnter
from rag import web_scrapping  

engine = create_engine("mysql+pymysql://uynrkcc9e4pxlhr3:l3tvSPxDBQ4AWrDQZRu@bzuq0tqc5ec6ynd5spke-mysql.services.clever-cloud.com:20037/bzuq0tqc5ec6ynd5spke")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
#no fue pa tando
class User(Base):
    __tablename__ = "users"  # ajusta si tu tabla se llama distinto

    # uuid VARCHAR(36) PRIMARY KEY
    uuid: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())  # genera 'xxxxxxxx-xxxx-...'
    )
    usuario: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    contrasena: Mapped[str] = mapped_column(String(255), nullable=False)

def get_session():
    return SessionLocal()


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
@app.post("/human")
async def human(entrance: HumanEntrance):
    mensaje = entrance.message
    humanAi = HumanAiConexion()
    return await humanAi.conectar(mensaje)

@app.post("/emotion")
async def emotion(entrance: EmotionEntrance):
    message = entrance.message
    emotion = EmotionConexion()
    return await emotion.conectar(message)


@app.get("/getEmotion/{emotion}")
async def get_emotion(emotion: str):
    emo = EmotionConexion()
    id = emotion
    return await emo.get_emotion(id)

@app.post("/register")
async def register(register:RegisterEnter):
    """Crea un usuario. Lanza excepción si falla (por ejemplo, duplicado)."""
    session = get_session()
    try:
        u = User(uuid=str(uuid.uuid4()), usuario=register.username, contrasena=register.password)
        session.add(u)
        session.commit()
        session.refresh(u)
        return u
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# --- 2. NUEVO ENDPOINT PARA GENERAR GUIONES CON RAG ---
@app.post("/create-hybrid-lesson-plan/", response_model=HybridLesson)
async def create_hybrid_lesson_plan(topic: str):
    """
    Genera un plan de lección estructurado para un videotutorial híbrido, usando RAG.
    """
    try:
        # 1. Conectamos a la base de datos RAG
        rag_db = web_scrapping.AutoRAGDB()
        
        # 2. Buscamos fragmentos de texto relevantes
        relevant_fragments = rag_db.search_fragments_by_query(topic, top_k=5)
        
        # 3. Cerramos la conexión a la base de datos
        rag_db.close()
        
        # 4. Formateamos el contexto para inyectarlo en el prompt
        rag_context = "\n".join([f"Fragmento: {text}\nFuente: {source}" for text, source in relevant_fragments])

        # 5. Creamos un prompt de sistema muy específico para guiar a la IA
        system_prompt = f"""
        Eres un guionista experto para tutoriales de IA en YouTube.
        Tu tarea es crear el guion para un video de 5 minutos sobre el tema: "{topic}".
        El video tiene un formato Híbrido: primero explica la teoría y luego muestra cómo aplicarla con código.
        Usa la siguiente información de contexto para fundamentar tu explicación. Si la información no es relevante, ignórala.

        --- CONTEXTO RAG ---
        {rag_context}
        --- FIN DEL CONTEXTO ---

        Debes devolver tu respuesta exclusivamente en formato JSON, siguiendo esta estructura exacta:

        {{
          "title": "string",
          "theory_script": "string",
          "bridge_script": "string",
          "tooling_script_steps": ["string", "string", "..."]
        }}
        """

        # 6. Usamos tu clase de conexión existente
        conexion = ChatGptConexion()
        response_from_api = await conexion.conectar(system_prompt)

        # 7. La respuesta de la API puede venir como un string o ya como un diccionario.
        # Nos aseguramos de que sea un diccionario para poder trabajarlo.
        if isinstance(response_from_api, str):
            lesson_data = json.loads(response_from_api)
        else:
            lesson_data = response_from_api
        
        # 8. Pydantic usa el diccionario para crear y validar nuestro objeto HybridLesson
        lesson_plan = HybridLesson(**lesson_data)
        
        return lesson_plan

    except Exception as e:
        # Manejo de errores por si la API falla o el JSON es inválido
        raise HTTPException(status_code=500, detail=f"Error al generar el plan de lección: {str(e)}")

@app.post("/human")
async def human(entrance: HumanEntrance):
    mensaje = entrance.message
    humanAi = HumanAiConexion()
    return await humanAi.conectar(mensaje)
