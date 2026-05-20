from backend.rag.vector_store import vector_store

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

def retrieve_docs(query):

    docs = retriever.invoke(query)

    return "\n\n".join([

        doc.page_content

        for doc in docs

    ])