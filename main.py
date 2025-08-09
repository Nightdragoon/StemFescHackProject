from fastapi import FastAPI

from ChatGptEntranceDto import ChatGptEntranceDto
from ChatGptConexion import ChatGptConexion
from HumanEntrance import HumanEntrance

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

@app.post("/human")
async def human(entrance: HumanEntrance):
    mensaje = entrance.message
    humanAi = HumanEntrance()
    conexion = humanAi.conectar(mensaje)





