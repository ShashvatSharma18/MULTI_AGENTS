from langchain_chroma import Chroma

from backend.rag.embeddings import embeddings


# =========================================================
# VECTOR STORE
# =========================================================

vector_store = Chroma(
    collection_name="multi_agent_rag",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)