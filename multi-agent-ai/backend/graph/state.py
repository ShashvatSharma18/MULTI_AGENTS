from typing import TypedDict, List, Dict, Any

# =========================================================
# STATE
# =========================================================

class State(TypedDict):
    question: str
    result: str
    results: Dict[str, Any]
    next_agents: List[str]
    sub_tasks: List[Dict[str, str]] # [{ "agent": "...", "task_query": "..." }]
    resume_text: str
    messages: List[dict]
    reasoning: List[Dict[str, Any]]
    token_usage: Dict[str, Any]
