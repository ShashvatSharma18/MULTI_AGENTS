from langchain_groq import ChatGroq
from backend.config.settings import MAIN_GROQ_API_KEY, GROQ_API_KEY

# =========================================================
# MAIN LLM
# =========================================================

llm = ChatGroq(
    groq_api_key=MAIN_GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)


# =========================================================
# CODING LLM
# =========================================================

coding_llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.5
)
