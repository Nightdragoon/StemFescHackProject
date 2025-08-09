import requests
import json

class HumanAiConexion:
    async def conectar(self, mensaje: str):
        url = "https://api.hume.ai/v0/tts/stream/json"

        payload = json.dumps({
            "utterances": [
                {
                    "text": mensaje,
                    "voice": {
                        "name": "Male English Actr",
                        "provider": "HUME_AI"
                    }
                }
            ]
        })
        headers = {
            'X-Hume-Api-Key': 'zsocslq2FcOflqLZWRANKPB6NUDiLQXP3mQPGH90AMeQ7DHm',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()