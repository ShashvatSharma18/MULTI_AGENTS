# =========================================================
# backend/graph/orchestrator.py
# =========================================================

from backend.agents.weather_agent import weather_agent
from backend.agents.resume_agent import resume_agent
from backend.agents.coding_agent import coding_agent
from backend.agents.fallback_agent import fallback_agent
from backend.graph.state import State

import time

def orchestrator_node(state: State):
    print("\n[DEBUG] ORCHESTRATOR STARTED")
    results = {}
    reasoning = state.get("reasoning", [])
    sub_tasks = state.get("sub_tasks", [])
    
    print(f"[DEBUG] SUB TASKS TO RUN: {sub_tasks}")
    
    for task_info in sub_tasks:
        agent = task_info["agent"]
        task_query = task_info["task_query"]
        
        # Create a temporary local state for the agent call
        local_state = state.copy()
        local_state["question"] = task_query # Override global question with specific sub-task
        
        print(f"[DEBUG] RUNNING: {agent} for task: {task_query}")
        
        start_time = time.time()
        
        if agent == "weather_agent":
            output = weather_agent(local_state)
        elif agent == "resume_agent":
            output = resume_agent(local_state)
        elif agent == "coding_agent":
            output = coding_agent(local_state)
        elif agent == "fallback_agent":
            output = fallback_agent(local_state)
        else:
            output = fallback_agent(local_state)
            
        print(f"OUTPUT for {agent}:", output)
            
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        # Save individual agent result
        results[agent] = output.get("result", "")
        
        reasoning.append({
            "step": "execution",
            "agent": agent,
            "task": task_query,
            "status": "success",
            "latency": f"{latency}s"
        })
        
    return {
        "results": results,
        "reasoning": reasoning
    }