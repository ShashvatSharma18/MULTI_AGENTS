from dotenv import load_dotenv
load_dotenv()

import os
import requests
import re
import streamlit as st

from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langsmith import traceable

# ---------------- ENV ----------------
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"

print("TRACING:", os.getenv("LANGCHAIN_TRACING_V2"))
print("PROJECT:", os.getenv("LANGCHAIN_PROJECT"))

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Multi Agent AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
    font-size: 18px;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">🤖 Multi Agent AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">LangGraph + LangChain + LangSmith</div>',
    unsafe_allow_html=True
)

# ---------------- STATE ----------------
class State(TypedDict):
    question: str
    result: str
    next: str
    resume_text: str

# ---------------- API KEYS ----------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("OPENROUTER:", OPENROUTER_API_KEY)
print("GROQ:", GROQ_API_KEY)

# ---------------- MAIN LLM ----------------
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="meta-llama/llama-3.1-8b-instruct",
    streaming=True,
    temperature=0.7
)

# ---------------- CODING LLM ----------------
coding_llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    streaming=True,
    temperature=0.5
)

# ---------------- STREAM FUNCTION ----------------
def stream_llm_response(llm_model, prompt):

    response = llm_model.stream(prompt)

    full_response = ""

    for chunk in response:

        if chunk.content:

            full_response += chunk.content

            yield full_response

# ---------------- WEATHER TOOL ----------------
@tool
def get_weather(city: str) -> str:
    """Get current weather of city"""

    api_key = "YOUR_WEATHER_API_KEY"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:

        response = requests.get(url)

        data = response.json()

        if response.status_code != 200:
            return "❌ City not found"

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        return f"🌤️ Weather in {city}: {temp}°C, {weather}"

    except Exception as e:
        return f"❌ Weather Error: {str(e)}"

# ---------------- SUPERVISOR ----------------
def supervisor_node(state: State):

    question = state["question"]

    router_prompt = f"""
You are a strict classifier.

Classify the query into ONLY one:

weather_agent
resume_agent
coding_agent
fallback_agent

Rules:
- coding/debugging/programming -> coding_agent
- resume/cv/job/ats -> resume_agent
- weather/rain/temp -> weather_agent
- greetings/general -> fallback_agent

ONLY return agent name.

User Query:
{question}
"""

    response = llm.invoke(router_prompt)

    next_agent = response.content.strip().lower()

    next_agent = next_agent.split()[0]
    next_agent = next_agent.replace(".", "")
    next_agent = next_agent.replace("-", "_")

    valid_agents = {
        "weather_agent",
        "resume_agent",
        "coding_agent",
        "fallback_agent"
    }

    if next_agent not in valid_agents:
        next_agent = "fallback_agent"

    print("ROUTED TO:", next_agent)

    return {
        "next": next_agent
    }

# ---------------- WEATHER AGENT ----------------
def weather_agent(state: State):

    question = state["question"]

    city_match = re.findall(
        r"(?:in|of)\s+([A-Za-z ]+)",
        question
    )

    city = city_match[0].strip() if city_match else "Delhi"

    result = get_weather.invoke({
        "city": city
    })

    return {
        "result": result
    }

# ---------------- RESUME AGENT ----------------
def resume_agent(state: State):

    resume_text = state["resume_text"]

    if not resume_text:

        return {
            "result": "📄 Please upload your resume PDF first."
        }

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume professionally.

Provide:
1. ATS Score
2. Skills Analysis
3. Missing Skills
4. Resume Improvements
5. Interview Tips
6. Suggested Projects

Resume:
{resume_text}
"""

    stream_generator = stream_llm_response(
        llm,
        prompt
    )

    return {
        "result": stream_generator
    }

# ---------------- CODING AGENT ----------------
def coding_agent(state: State):

    question = state["question"]

    prompt = f"""
You are an expert coding assistant.

Help user with:
- coding
- debugging
- DSA
- algorithms
- optimization
- explanations

User Question:
{question}
"""

    stream_generator = stream_llm_response(
        coding_llm,
        prompt
    )

    return {
        "result": stream_generator
    }

# ---------------- FALLBACK AGENT ----------------
def fallback_agent(state: State):

    question = state["question"]

    prompt = f"""
You are a helpful AI assistant.

User Question:
{question}

Give a professional and clear response.
"""

    stream_generator = stream_llm_response(
        llm,
        prompt
    )

    return {
        "result": stream_generator
    }

# ---------------- BUILD GRAPH ----------------
builder = StateGraph(State)

builder.add_node("supervisor", supervisor_node)

builder.add_node("weather_agent", weather_agent)
builder.add_node("resume_agent", resume_agent)
builder.add_node("coding_agent", coding_agent)
builder.add_node("fallback_agent", fallback_agent)

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],
    {
        "weather_agent": "weather_agent",
        "resume_agent": "resume_agent",
        "coding_agent": "coding_agent",
        "fallback_agent": "fallback_agent"
    }
)

builder.add_edge("weather_agent", END)
builder.add_edge("resume_agent", END)
builder.add_edge("coding_agent", END)
builder.add_edge("fallback_agent", END)

graph = builder.compile()

# ---------------- TRACE ----------------
@traceable(name="multi-agent-run")
def run_graph(inputs):
    return graph.invoke(inputs)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    resume_text = ""

    if uploaded_file is not None:

        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())

        loader = PyPDFLoader("temp_resume.pdf")

        pages = loader.load()

        resume_text = "\n".join([
            page.page_content for page in pages
        ])

        st.success("✅ Resume Uploaded Successfully")

    st.divider()

    st.markdown("### 💡 Example Questions")

    st.markdown("- What is weather in Delhi?")
    st.markdown("- Analyze my resume")
    st.markdown("- Write merge sort in python")
    st.markdown("- Explain binary search")

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY HISTORY ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Ask Anything...")

if prompt and prompt.strip() != "":

    # ---------------- SAVE USER MESSAGE ----------------
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- ASSISTANT ----------------
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        complete_text = ""

        # =====================================================
        # LIVE OVERVIEW INSIDE SAME RESPONSE AREA
        # =====================================================

        overview_prompt = f"""
You are an intelligent AI assistant.

User Question:
{prompt}

Generate natural thinking before answering.

Rules:
- Think naturally
- Sound intelligent
- Explain what you are understanding
- Do NOT fully answer
- Do NOT use headings like Overview
- Keep it conversational
- Make it feel like real-time reasoning
"""

        overview_stream = llm.stream(overview_prompt)

        for chunk in overview_stream:

            if chunk.content:

                complete_text += chunk.content

                response_placeholder.markdown(complete_text)

        # natural transition
        complete_text += "\n\n"

        response_placeholder.markdown(complete_text)

        # =====================================================
        # MAIN GRAPH RESPONSE
        # =====================================================

        response = run_graph({
            "question": prompt,
            "resume_text": resume_text
        })

        result = response.get("result")

        # =====================================================
        # STREAM MAIN ANSWER LIVE
        # =====================================================

        if hasattr(result, "__iter__") and not isinstance(result, str):

            previous_length = 0

            for chunk in result:

                new_text = chunk[previous_length:]

                previous_length = len(chunk)

                complete_text += new_text

                response_placeholder.markdown(complete_text)

        else:

            complete_text += str(result)

            response_placeholder.markdown(complete_text)

    # ---------------- SAVE ASSISTANT RESPONSE ----------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": complete_text
    })