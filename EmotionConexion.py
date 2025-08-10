from pydantic import BaseModel
import requests
import json

class EmotionConexion(BaseModel):

    async def get_emotion(self, emotion: str):
        url = "https://api.hume.ai/v0/batch/jobs/" + emotion + "/predictions"

        payload = {}
        headers = {
            'X-Hume-Api-Key': 'zsocslq2FcOflqLZWRANKPB6NUDiLQXP3mQPGH90AMeQ7DHm'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    async def conectar(self, mensaje: str):
        url = "https://api.hume.ai/v0/batch/jobs"

        payload = json.dumps({
            "models": {
                "language": {
                    "granularity": "utterance",
                    "sentiment": None
                }
            },
            "text": [
                "i am very exited for tomorrow omg i love this"
            ],
            "notify": False
        })
        headers = {
            'X-Hume-Api-Key': 'zsocslq2FcOflqLZWRANKPB6NUDiLQXP3mQPGH90AMeQ7DHm',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

