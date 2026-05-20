from backend.models.llm import llm
from backend.prompts.resume_prompt import RESUME_PROMPT

# =========================================================
# RESUME AGENT
# =========================================================

def resume_agent(state):

    resume_text = state.get("resume_text", "")

    retrieved_docs = state.get(
        "retrieved_docs",
        ""
    )

    if not resume_text.strip():

        return {
            "result": "📄 Please upload your resume PDF first."
        }

    history = "\n".join([

        f"{m['role']}: {m['content']}"

        for m in state["messages"]

    ])

    # =====================================================
    # USE RESUME PROMPT TEMPLATE
    # =====================================================

    # Use retrieved_docs if available, otherwise full resume
    context = retrieved_docs if retrieved_docs.strip() else resume_text

    prompt = RESUME_PROMPT.format(
        history=history,
        resume_text=context
    )

    response = llm.invoke(prompt)

    return {
        "result": response.content
    }