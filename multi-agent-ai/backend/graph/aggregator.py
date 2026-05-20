# =========================================================
# backend/graph/aggregator.py
# =========================================================
from backend.graph.state import State

import json

def aggregator_node(state: State):
    results = state["results"]
    print("AGGREGATOR RESULTS:", results)
    reasoning = state.get("reasoning", [])
    
    # Combine results from multiple agents
    final_responses = []
    for agent, text in results.items():
        header = f"## {agent.replace('_', ' ').title()}"
        final_responses.append(f"{header}\n\n{text}")
        
    final_text = "\n\n---\n\n".join(final_responses)
    
    if not final_text:
        final_text = "I couldn't gather any specific information for your request."
    
    reasoning.append({
        "step": "aggregation",
        "message": f"Combined results from {len(results)} agents.",
        "status": "success"
    })
    
    print("\n========== STRUCTURED REASONING ==========\n")
    print(json.dumps(reasoning, indent=2))
    print("\n==========================================\n")
    
    return {
        "result": final_text,
        "reasoning": reasoning
    }
