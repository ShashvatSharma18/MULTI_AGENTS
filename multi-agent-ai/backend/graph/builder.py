from langgraph.graph import StateGraph, END
from langsmith import traceable
from langgraph.checkpoint.memory import MemorySaver

from backend.graph.state import State
from backend.agents.supervisor import supervisor_node
from backend.graph.rag_node import rag_node
from backend.graph.orchestrator import orchestrator_node
from backend.graph.aggregator import aggregator_node

# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(State)

builder.add_node("supervisor", supervisor_node)
builder.add_node("orchestrator", orchestrator_node)
builder.add_node("aggregator", aggregator_node)

builder.set_entry_point("supervisor")

builder.add_edge("supervisor", "orchestrator")
builder.add_edge("orchestrator", "aggregator")
builder.add_edge("aggregator", END)

graph = builder.compile() # Checkpointer disabled for debug

# =========================================================
# TRACE EXPORT
# =========================================================

@traceable(name="multi-agent-run")
def run_graph(inputs, config=None):
    print("[DEBUG] GRAPH EXECUTION STARTED")
    res = graph.invoke(inputs, config=config)
    print("[DEBUG] GRAPH EXECUTION FINISHED")
    return res
