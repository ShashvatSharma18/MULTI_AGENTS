from langchain_community.document_loaders import PyPDFLoader, TextLoader

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from backend.rag.vector_store import (
    vector_store
)

# =========================================================
# TEXT SPLITTER
# =========================================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=200

)

# =========================================================
# INGEST PDF
# =========================================================

def ingest_pdf(file_path):

    loader = PyPDFLoader(file_path)

    pages = loader.load()

    docs = splitter.split_documents(pages)

    vector_store.add_documents(docs)

    print(f"✅ Stored {len(docs)} PDF chunks in ChromaDB")

    return docs

# =========================================================
# INGEST TXT
# =========================================================

def ingest_text(file_path):

    loader = TextLoader(file_path, encoding="utf-8")

    pages = loader.load()

    docs = splitter.split_documents(pages)

    vector_store.add_documents(docs)

    print(f"✅ Stored {len(docs)} TXT chunks in ChromaDB")

    return docs