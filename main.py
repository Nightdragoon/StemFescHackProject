from fastapi import FastAPI

from ChatGptEntranceDto import ChatGptEntranceDto
from ChatGptConexion import ChatGptConexion

app = FastAPI()


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


