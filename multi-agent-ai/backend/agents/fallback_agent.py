from backend.models.llm import llm
from backend.prompts.fallback_prompt import FALLBACK_PROMPT

# =========================================================
# FALLBACK AGENT
# =========================================================

def fallback_agent(state):

    question = state["question"]

    retrieved_docs = state.get(
        "retrieved_docs",
        ""
    )

    history = "\n".join([

        f"{m['role']}: {m['content']}"

        for m in state["messages"]

    ])

    # =====================================================
    # USE FALLBACK PROMPT TEMPLATE
    # =====================================================

    prompt = FALLBACK_PROMPT.format(
        history=history,
        question=question
    )

    # =====================================================
    # APPEND RAG CONTEXT IF AVAILABLE
    # =====================================================

    if retrieved_docs.strip():
        prompt += f"\n\nRetrieved Document Content:\n{retrieved_docs}"

    response = llm.invoke(prompt)

    return {
        "result": response.content
    }