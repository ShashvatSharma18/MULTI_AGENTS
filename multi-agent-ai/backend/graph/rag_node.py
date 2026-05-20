from backend.rag.retriever import retriever

# =========================================================
# RAG NODE
# =========================================================

def rag_node(state):

    question = state["question"]

    docs = retriever.invoke(question)

    retrieved_text = "\n\n".join([

        doc.page_content

        for doc in docs

    ])

    return {
        "retrieved_docs": retrieved_text
    }