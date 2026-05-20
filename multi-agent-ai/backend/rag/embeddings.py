from sentence_transformers import SentenceTransformer


# =========================================================
# LOCAL EMBEDDING MODEL
# =========================================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# CUSTOM EMBEDDINGS CLASS
# =========================================================

class LocalEmbeddings:

    def embed_documents(self, texts):

        embeddings = embedding_model.encode(texts)

        return embeddings.tolist()

    def embed_query(self, text):

        embedding = embedding_model.encode(text)

        return embedding.tolist()


embeddings = LocalEmbeddings()