import os
from langchain_community.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embeddings import SentenceTransformerEmbeddings

# Importa tus scrapers
from scrape_mit import scrape_mit_ocw_courses
from scrape_github import scrape_github_repos
from scrape_arxiv import scrape_arxiv_api
from scrape_docsIA import scrape_docsIA   # <-- Import agregado

INDEX_PATH = "faiss_index"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

class AutoRAG:
    def __init__(self):
        print(f"🤖 Cargando modelo embeddings '{MODEL_NAME}'...")
        self.embeddings = SentenceTransformerEmbeddings(MODEL_NAME)
        self.vectorstore = None
        self.load_or_create_index()

    def load_or_create_index(self):
        if os.path.exists(INDEX_PATH):
            try:
                self.vectorstore = FAISS.load_local(
                    INDEX_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                print("✅ Índice cargado desde disco")
            except Exception as e:
                print(f"❌ Error cargando índice: {e}")
                self.create_new_index()
        else:
            self.create_new_index()

    def create_new_index(self):
        import faiss
        dimension = self.embeddings.model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(dimension)
        self.vectorstore = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore({}),
            index_to_docstore_id={},
        )
        print("🆕 Nuevo índice creado")

    def fetch_and_index(self):
        print("🔄 Ejecutando scrapers y preparando datos...")

        mit_docs = scrape_mit_ocw_courses()
        github_docs = scrape_github_repos()
        arxiv_docs = scrape_arxiv_api()
        docsIA_docs = scrape_docsIA()   # <-- Scraper agregado

        all_texts = []

        for doc in mit_docs:
            text = (doc.get("description") or "") + " " + (doc.get("title") or "")
            if text.strip():
                all_texts.append(text.strip())

        for doc in github_docs:
            text = (doc.get("description") or "") + " " + (doc.get("readme_excerpt") or "")
            if text.strip():
                all_texts.append(text.strip())

        for doc in arxiv_docs:
            text = (doc.get("title") or "") + " " + (doc.get("abstract") or "")
            if text.strip():
                all_texts.append(text.strip())

        for doc in docsIA_docs:
            # Aquí adaptas según qué campos devuelve scrape_docsIA()
            # Por ejemplo, si devuelve {'content': "..."}:
            text = doc.get("content") or doc.get("text") or ""
            if text.strip():
                all_texts.append(text.strip())

        if not all_texts:
            print("⚠️ No hay texto para indexar.")
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text("\n\n".join(all_texts))

        print(f"📚 Generando embeddings para {len(chunks)} fragmentos...")
        self.vectorstore.add_texts(chunks)
        self.vectorstore.save_local(INDEX_PATH)
        print("✅ Índice actualizado y guardado.")

    def query(self, texto):
        if not self.vectorstore or self.vectorstore.index.ntotal == 0:
            return "⚠️ Índice vacío, ejecuta fetch_and_index() primero."

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(texto)
        return "\n---\n".join([d.page_content for d in docs])

if __name__ == "__main__":
    rag = AutoRAG()
    rag.fetch_and_index()

    while True:
        pregunta = input("\n❓ Haz tu pregunta (o 'salir' para terminar): ")
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            break
        respuesta = rag.query(pregunta)
        print(f"\n💬 Respuesta:\n{respuesta}")
