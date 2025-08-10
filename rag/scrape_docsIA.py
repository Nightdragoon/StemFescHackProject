import requests
from bs4 import BeautifulSoup
import re
import os

from mistralai import Mistral  # Asegúrate de tener la librería y variable de entorno configurada
from dotenv import load_dotenv

load_dotenv()

# URLs de docs oficiales para scrapear texto
urls = {
    "LangChain": "https://python.langchain.com/docs",
    "HuggingFace": "https://huggingface.co/docs",
    "Vercel AI SDK": "https://vercel.com/docs",
    "Cursor": "https://cursor.so/docs",
}

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def scrape_text_from_url(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Extraer párrafos y títulos para un resumen
        texts = []
        for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            t = clean_text(tag.get_text())
            if len(t) > 20:
                texts.append(t)
        return texts
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return []

def resumir_texto_mistral(textos):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró la variable de entorno MISTRAL_API_KEY")
        return "No se pudo generar resumen"

    client = Mistral(api_key=api_key)

    # Usar solo primeros 10 textos para no saturar
    input_text = "\n".join(textos[:10])
    prompt = (
        "Genera un resumen breve y claro de esta documentación oficial para entender de qué trata:\n\n"
        f"{input_text}\n\n"
        "Resumen:"
    )
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.complete(model="mistral-small-latest", messages=messages)
        resumen = response.choices[0].message.content.strip()
        return resumen
    except Exception as e:
        print(f"❌ Error generando resumen con Mistral: {e}")
        return "No se pudo generar resumen"

def main():
    all_docs = []
    for name, url in urls.items():
        print(f"🌐 Extrayendo contenido de {name}...")
        textos = scrape_text_from_url(url)
        descripcion = resumir_texto_mistral(textos)
        print(f"📝 Resumen para {name}: {descripcion}")

        for texto in textos:
            all_docs.append({
                "source": name,
                "url": url,
                "description": descripcion,
                "content": texto
            })
    return all_docs

if __name__ == "__main__":
    docs = main()
    print(f"✅ Total fragmentos extraídos: {len(docs)}")
    # Puedes hacer algo con docs aquí, por ejemplo, imprimir un fragmento o pasar a embedding
