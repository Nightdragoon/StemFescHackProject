import os
import pickle
import sys
from datetime import datetime
import numpy as np
from scipy.spatial.distance import cosine

from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Importar la clase de embeddings de OpenAI
from langchain_openai import OpenAIEmbeddings

# Importar para cargar las variables de entorno desde un archivo .env
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Asegurar que el path del proyecto esté disponible para importar otros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa scrapers tuyos (descomenta los que necesites)
from rag.scrape_mit import scrape_mit_ocw_courses
from rag.scrape_github import main as github_main
from rag.scrape_arxiv import scrape_arxiv_api
from rag.scrape_docsIA import main as docsia_main

# Configuración DB
DATABASE_URL = "mysql+pymysql://uynrkcc9e4pxlhr3:l3tvSPxDBQ4AWrDQZRu@bzuq0tqc5ec6ynd5spke-mysql.services.clever-cloud.com:20037/bzuq0tqc5ec6ynd5spke"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para rag_fragments
class RAGFragment(Base):
    __tablename__ = "rag_fragments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_url = Column(String(512), nullable=True)
    fragment_text = Column(Text, nullable=False, unique=True)
    embedding = Column(LargeBinary, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

Base.metadata.create_all(bind=engine)

class AutoRAGDB:
    def __init__(self):

        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.session = SessionLocal()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    def fetch_and_index_to_db(self):
        print("🔄 Ejecutando scrapers y preparando datos para DB...")

        # Ejecutar scrapers
        mit_docs = scrape_mit_ocw_courses()
        github_docs = github_main()
        arxiv_docs = scrape_arxiv_api()
        docsIA_docs = docsia_main()

        all_texts = []
        all_sources = []

        # Agregar textos y fuente (link u origen) si existe
        for doc in mit_docs:
            text = (doc.get("description") or "") + " " + (doc.get("title") or "")
            if text.strip():
                all_texts.append(text.strip())
                all_sources.append(doc.get("link") or None)

        for doc in github_docs:
            text = (doc.get("description") or "") + " " + (doc.get("readme_excerpt") or "")
            if text.strip():
                all_texts.append(text.strip())
                all_sources.append(doc.get("url") or None)
        
        for doc in arxiv_docs:
            text = (doc.get("title") or "") + " " + (doc.get("abstract") or "")
            if text.strip():
                all_texts.append(text.strip())
                all_sources.append(doc.get("pdf_link") or None)

        for doc in docsIA_docs:
            text = doc.get("content") or doc.get("text") or ""
            if text.strip():
                all_texts.append(text.strip())
                all_sources.append(doc.get("url") or None)


        if not all_texts:
            print("⚠️ No hay texto para indexar.")
            return

        print(f"🔪 Dividiendo {len(all_texts)} documentos en fragmentos...")
        all_chunks = []
        all_chunk_sources = []

        for text, src in zip(all_texts, all_sources):
            chunks = self.splitter.split_text(text)
            all_chunks.extend(chunks)
            all_chunk_sources.extend([src] * len(chunks))

        print(f"📚 Generando embeddings para {len(all_chunks)} fragmentos con la API...")

        # Insertar o actualizar en la base de datos
        for chunk, source_url in zip(all_chunks, all_chunk_sources):
            # La llamada a la API está aquí
            embedding_vector = self.embeddings.embed_documents([chunk])[0]
            embedding_bytes = pickle.dumps(embedding_vector)

            existing = self.session.query(RAGFragment).filter_by(fragment_text=chunk).first()
            if existing:
                existing.embedding = embedding_bytes
                existing.updated_at = datetime.now()
                print(f"♻️ Actualizado fragmento existente")
            else:
                new_fragment = RAGFragment(
                    source_url=source_url,
                    fragment_text=chunk,
                    embedding=embedding_bytes,
                )
                self.session.add(new_fragment)
                print(f"➕ Insertado nuevo fragmento")

        self.session.commit()
        print(f"✅ Guardados {len(all_chunks)} fragmentos en la base de datos.")

    def search_fragments_by_query(self, query: str, top_k: int = 3):
        """
        Busca fragmentos de texto similares en la base de datos basándose en una consulta.
        Devuelve una lista de los fragmentos más relevantes.
        """
        print(f"🔎 Buscando fragmentos para la consulta: '{query}'")

        # 1. Generar el embedding para la consulta
        # Esta llamada también usa la API de OpenAI
        query_embedding_vector = self.embeddings.embed_documents([query])[0]
        query_embedding_np = np.array(query_embedding_vector)

        # 2. Recuperar todos los fragmentos y sus embeddings
        all_fragments = self.session.query(RAGFragment).all()

        # 3. Calcular la similitud del coseno
        similarities = []
        for fragment in all_fragments:
            stored_embedding_vector = pickle.loads(fragment.embedding)
            stored_embedding_np = np.array(stored_embedding_vector)
            
            # La distancia del coseno es 1 - similitud. Cuanto más cerca de 0, más similar.
            similarity = 1 - cosine(query_embedding_np, stored_embedding_np)
            similarities.append((similarity, fragment.fragment_text, fragment.source_url))
        
        # 4. Ordenar por similitud y obtener los 'top_k' resultados
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_fragments = [ (text, source) for sim, text, source in similarities[:top_k] ]

        print(f"✅ Encontrados {len(top_fragments)} fragmentos relevantes.")
        return top_fragments

    def close(self):
        self.session.close()

if __name__ == "__main__":
    rag_db = AutoRAGDB()
    rag_db.fetch_and_index_to_db()
    rag_db.close()
