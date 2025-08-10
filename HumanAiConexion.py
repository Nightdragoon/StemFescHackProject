from asyncio.windows_events import NULL

import requests
import json

class HumanAiConexion:

    def _split_concatenated_json(self ,text: str):
        """Convierte '{}{}[]{}' o '[{},{},...]' en una lista de objetos."""
        dec = json.JSONDecoder()
        s = text.strip()
        out = []
        while s:
            obj, j = dec.raw_decode(s)
            if isinstance(obj, list):
                out.extend(obj)
            else:
                out.append(obj)
            s = s[j:].lstrip()
        return out

    async def conectar(self, mensaje: str):
       try:
           url = "https://api.hume.ai/v0/tts"

           payload = json.dumps({
               "utterances": [
                   {
                       "text": mensaje,
                       "voice": {
                           "name": "Mysterious Woman",
                           "provider": "HUME_AI"
                       }
                   }
               ]
           })
           headers = {
               'X-Hume-Api-Key': 'zsocslq2FcOflqLZWRANKPB6NUDiLQXP3mQPGH90AMeQ7DHm',
               'Content-Type': 'application/json'
           }
           response = requests.request("POST", url, headers=headers, data=payload , stream=True)

           return response.json()


       except Exception as e:
           return NULL