import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import csv
import time
import os

from dotenv import load_dotenv

load_dotenv()
# -- Llave API Mistral esperada en variable de entorno MISTRAL_API_KEY --

KEYWORDS_BASE = [
    "artificial intelligence", "machine learning",
    "deep learning", "neural networks", "cnn", "rnn", "transfer learning",
    "plm", "language models", "transformers", "attention", "gan",
    "optimization algorithms", "adam", "sgd", "regularization", "dropout",
    "fine-tuning", "overfitting", "cross-validation", "dimensionality reduction",
    "pca", "rag", "retrieval-augmented generation", "semantic search",
    "vector databases", "faiss", "annoy", "hnsw", "knn", "text embeddings",
    "embeddings", "dataset", "tokenization", "word2vec", "glove", "feature extraction",
    "AI"
]

CSV_FILE = "arxiv_filtered_papers.csv"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def contains_keywords_regex(text, keywords):
    text = text.lower()
    patterns = [re.compile(r'\b' + re.escape(kw.lower()) + r'\b') for kw in keywords]
    for pattern in patterns:
        if pattern.search(text):
            return True
    return False

def consultar_llm(prompt: str):
    try:
        from mistralai import Mistral
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            print("❌ Error: No se encontró la variable de entorno MISTRAL_API_KEY")
            return None
        client = Mistral(api_key=api_key)
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.complete(model="mistral-small-latest", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error llamando a Mistral: {e}")
        return None

def generar_palabras_clave_nuevas(abstracts, max_keywords=20):
    texto = "\n\n".join(abstracts[:50])  # tomar máximo 50 abstracts para no saturar
    prompt = (
        "Analiza los siguientes abstracts de papers de Inteligencia Artificial:\n\n"
        f"{texto}\n\n"
        "Extrae una lista de palabras clave relevantes y actuales para el área de IA y aprendizaje automático, "
        f"separadas por comas. Limita la lista a {max_keywords} palabras clave que no estén en la lista base.\n"
        "Responde solo con las palabras clave, sin explicaciones."
    )
    respuesta = consultar_llm(prompt)
    if respuesta:
        nuevas = [kw.strip().lower() for kw in respuesta.split(",")]
        nuevas = list(set([kw for kw in nuevas if kw and kw not in [k.lower() for k in KEYWORDS_BASE]]))
        print(f"✨ Mistral sugirió {len(nuevas)} nuevas palabras clave: {nuevas}")
        return nuevas
    else:
        return []

def parse_arxiv_response(xml_text):
    soup = BeautifulSoup(xml_text, "xml")
    entries = soup.find_all('entry')
    papers = []
    for entry in entries:
        paper_id = entry.id.text.split('/')[-1]
        title = clean_text(entry.title.text)
        authors = ", ".join([author.find('name').text for author in entry.find_all('author')])
        abstract = clean_text(entry.summary.text)
        date = entry.published.text
        pdf_link = None
        for link in entry.find_all('link'):
            if link.get('title') == 'pdf':
                pdf_link = link.get('href')
                break
        papers.append({
            "paper_id": paper_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "date": date,
            "pdf_link": pdf_link
        })
    return papers

def scrape_arxiv_api(min_papers=100, query="cat:cs.AI"):
    print(f"🔍 Scraping arXiv con query '{query}', buscando {min_papers} papers...")
    collected = []
    start = 0
    max_results = 100
    keywords = KEYWORDS_BASE.copy()  # lista fija para filtrar
    abstracts_for_llm = []
    nuevas_keywords_report = []  # solo para reporte

    while len(collected) < min_papers:
        url = (
            "http://export.arxiv.org/api/query?"
            f"search_query={query}&start={start}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        )
        print(f"📄 Consultando API arXiv: start={start}")
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"⚠️ Error HTTP {resp.status_code} en consulta arXiv")
            break

        papers = parse_arxiv_response(resp.text)
        if not papers:
            print("⚠️ No hay más resultados del API")
            break

        found_in_batch = 0
        for p in papers:
            text_to_check = p['title'] + " " + p['abstract']
            if not contains_keywords_regex(text_to_check, keywords):
                continue
            if len(p['abstract']) < 100:
                continue

            collected.append(p)
            abstracts_for_llm.append(p['abstract'])
            found_in_batch += 1

            if len(collected) == 50:
                nuevas = generar_palabras_clave_nuevas(abstracts_for_llm)
                if nuevas:
                    nuevas_keywords_report.extend(nuevas)
                    nuevas_keywords_report = list(set(nuevas_keywords_report))
                    print(f"✨ Nuevas keywords para reporte (NO usadas para filtrar): {nuevas_keywords_report}")

            if len(collected) >= min_papers:
                break

        print(f"➕ Encontrados {found_in_batch} papers relevantes en este batch. Total acumulado: {len(collected)}")
        if found_in_batch == 0:
            print("⚠️ No se encontraron papers relevantes en este batch, se detiene.")
            break

        start += max_results
        time.sleep(1)

    if collected:
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["paper_id", "title", "authors", "abstract", "date", "pdf_link"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(collected)
        print(f"✅ Guardados {len(collected)} papers filtrados en '{CSV_FILE}'")

        if nuevas_keywords_report:
            print(f"✨ Nuevas keywords detectadas (solo reporte): {', '.join(nuevas_keywords_report)}")
    else:
        print("⚠️ No se encontraron papers que cumplan los filtros.")

    return collected

if __name__ == "__main__":
    scrape_arxiv_api()
