from backend.models.llm import coding_llm
from backend.prompts.coding_prompt import CODING_PROMPT

# =========================================================
# CODING AGENT
# =========================================================

def coding_agent(state):

    question = state["question"]

    history = "\n".join([
        f"{m['role']}: {m['content']}"
        for m in state["messages"]
    ])

    prompt = CODING_PROMPT.format(
        history=history,
        question=question
    )

    response = coding_llm.invoke(prompt)

    return {
        "result": response.content
    }
