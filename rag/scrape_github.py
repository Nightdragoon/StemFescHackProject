import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import time
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def mistral_generar_ideas(max_ideas=50, retries=3):
    try:
        from mistralai import Mistral
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            logging.error("No se encontró la variable de entorno MISTRAL_API_KEY")
            return []
        client = Mistral(api_key=api_key)

        prompt = (
            f"Genera una lista de {max_ideas} ideas, temas o tecnologías populares para desarrollo de software, "
            "inteligencia artificial, machine learning, big data, DevOps, cloud y áreas relacionadas. "
            "Solo lista las ideas separadas por comas, sin explicaciones."
        )
        messages = [{"role": "user", "content": prompt}]

        for attempt in range(retries):
            response = client.chat.complete(model="mistral-small-latest", messages=messages)
            texto = response.choices[0].message.content.strip()
            if texto:
                ideas = [idea.strip() for idea in texto.split(",") if idea.strip()]
                return ideas[:max_ideas]
            else:
                logging.warning(f"Intento {attempt+1} - respuesta vacía, reintentando...")
                time.sleep(2)
        logging.error("No se obtuvieron ideas tras varios intentos.")
        return []
    except Exception as e:
        logging.error(f"Error llamando a Mistral para generar ideas: {e}")
        return []

def mistral_buscar_repos(marca_o_tema, max_repos=3, retries=3):
    try:
        from mistralai import Mistral
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            logging.error("No se encontró la variable de entorno MISTRAL_API_KEY")
            return []
        client = Mistral(api_key=api_key)

        prompt = (
            f"Lista {max_repos} repositorios populares en GitHub relacionados con '{marca_o_tema}'. "
            "Devuelve solo la lista en formato 'usuario/repositorio', separados por comas, sin explicación."
        )
        messages = [{"role": "user", "content": prompt}]

        for attempt in range(retries):
            response = client.chat.complete(model="mistral-small-latest", messages=messages)
            texto = response.choices[0].message.content.strip()
            if texto:
                repos = re.findall(r'\b[\w\-]+/[\w\-]+\b', texto)
                return repos[:max_repos]
            else:
                logging.warning(f"Intento {attempt+1} - respuesta vacía, reintentando...")
                time.sleep(2)
        logging.error("No se obtuvieron repositorios tras varios intentos.")
        return []
    except Exception as e:
        logging.error(f"Error llamando a Mistral para buscar repos: {e}")
        return []

def scrape_github_repo(repo_full_name):
    url = f"https://github.com/{repo_full_name}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 404:
            logging.warning(f"Repositorio no encontrado: {repo_full_name}")
            return None
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        description_el = soup.find("p", {"class": "f4 my-3"})
        description = clean_text(description_el.text) if description_el else "No description"

        topics = [t.text.strip() for t in soup.select("a.topic-tag")]

        readme_el = soup.find(id="readme")
        readme_text = ""
        if readme_el:
            paragraphs = readme_el.find_all("p")
            readme_text = " ".join(clean_text(p.get_text()) for p in paragraphs[:3])

        combined_text = f"{description}. Topics: {', '.join(topics)}. README excerpt: {readme_text}"

        return {
            "repo": repo_full_name,
            "url": url,
            "description": description,
            "topics": ", ".join(topics),
            "readme_excerpt": readme_text,
            "combined_text": combined_text
        }
    except Exception as e:
        logging.error(f"Error scraping {repo_full_name}: {e}")
        return None

def main():
    logging.info("Generando lista de ideas/temas con Mistral...")
    ideas = mistral_generar_ideas(max_ideas=50)
    if not ideas:
        logging.warning("No se pudieron generar ideas.")
        return []

    logging.info(f"Mistral generó {len(ideas)} ideas.")
    data = []
    for idea in ideas:
        logging.info(f"Buscando repos relacionados con: '{idea}'")
        repos = mistral_buscar_repos(idea, max_repos=3)
        if not repos:
            logging.warning(f"No se encontraron repos para '{idea}'")
            continue

        for repo in repos:
            logging.info(f"Scrapeando repo {repo}...")
            info = scrape_github_repo(repo)
            if info:
                info["idea"] = idea
                data.append(info)

    if data:
        logging.info(f"Se recolectaron datos de {len(data)} repositorios.")
    else:
        logging.warning("No se pudo scrapear ningún repositorio.")
    return data

if __name__ == "__main__":
    repos_data = main()
    # Opcional: imprimir resumen
    for i, d in enumerate(repos_data, 1):
        print(f"{i}. Repo: {d['repo']}, Idea: {d['idea']}, URL: {d['url']}")
