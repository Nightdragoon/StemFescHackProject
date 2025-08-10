# from langchain_core.embeddings import Embeddings
# from sentence_transformers import SentenceTransformer

# class SentenceTransformerEmbeddings(Embeddings):
#     def __init__(self, model_name: str):
#         self.model = SentenceTransformer(model_name)

#     def embed_documents(self, texts: list[str]) -> list[list[float]]:
#         # texts: lista de strings, output: lista de listas de floats
#         embeddings = self.model.encode(texts, show_progress_bar=False)
#         return embeddings.tolist()

#     def embed_query(self, text: str) -> list[float]:
#         embedding = self.model.encode([text], show_progress_bar=False)[0]
#         return embedding.tolist()
