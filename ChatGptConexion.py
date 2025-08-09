import requests
import json
class ChatGptConexion:
    async def conectar(self , entrance: str):
        try:
            url = "https://api.openai.com/v1/responses"

            payload = json.dumps({
                "model": "gpt-5-mini",
                "input": entrance
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer <api>',
                'Cookie': '__cf_bm=wadOHC75oTyb81.B78qNehjpknMeyKxMTZP6LBPERNA-1754759962-1.0.1.1-hJW6Yv9893sVtqn0clE0D9.QEDSlQF.vMAu0JvaDq5otMYRlT6qC1AKeyqr3AaSdcOlaIc3qSJ4Z6WClRyxki_Ysexue7BikPX4BTWbqkaY; _cfuvid=5Hdx4I96ICuPq1zSeUpso6U0P35QvRRBHCe2IcDahbs-1754759962062-0.0.1.1-604800000'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            return response.json()
        except Exception as e:
            print(e.args)
            return 0
