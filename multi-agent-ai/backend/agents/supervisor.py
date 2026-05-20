# =========================================================
# backend/agents/supervisor.py
# =========================================================

from backend.models.llm import llm
from backend.prompts.supervisor_prompt import (
    SUPERVISOR_PROMPT
)
import time

# =========================================================
# VALID AGENTS
# =========================================================

VALID_AGENTS = [
    "weather_agent",
    "resume_agent",
    "coding_agent",
    "fallback_agent"
]

# =========================================================
# HELPER
# =========================================================

def add_reasoning(state, message):
    if "reasoning" not in state:
        state["reasoning"] = []
    
    # If the logic has changed messaging to be dicts, handle it
    if state["reasoning"] and isinstance(state["reasoning"][0], dict):
        state["reasoning"].append({
            "step": "logic",
            "message": message,
            "status": "success"
        })
    else:
        state["reasoning"].append(message)

# =========================================================
# SUPERVISOR NODE
# =========================================================

import json

def supervisor_node(state):
    try:
        print("\n[DEBUG] SUPERVISOR STARTED")
        question = state.get("question", "")
        print("[DEBUG] QUESTION:", question)
        
        # Initial reasoning for this step
        reasoning = state.get("reasoning", [])
        reasoning.append({
            "step": "supervisor",
            "message": f"Analyzing mission objective: {question[:40]}...",
            "status": "success"
        })
        
        prompt = SUPERVISOR_PROMPT.format(
            question=question
        )
        
        response = llm.invoke(prompt)
        raw_output = response.content.strip()
        
        print("[DEBUG] RAW LLM OUTPUT:", raw_output)
        
        # Parse JSON
        sub_tasks = []
        try:
            if "```json" in raw_output:
                raw_output = raw_output.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_output:
                raw_output = raw_output.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_output)
            sub_tasks = data.get("tasks", [])
            
        except Exception as json_err:
            print(f"[DEBUG] Multi-Intent JSON Parse Error: {json_err}. Falling back to default.")
            sub_tasks = [{"agent": "fallback_agent", "task_query": question}]

        # =====================================================
        # FALLBACK LOGIC
        # =====================================================
        if not sub_tasks:
            sub_tasks = [{"agent": "fallback_agent", "task_query": question}]
            reasoning.append({
                "step": "supervisor",
                "message": "No tasks identified → routing to fallback",
                "status": "success"
            })
            
        # Extract unique agent list for orchestration
        parsed_agents = list(set([t["agent"] for t in sub_tasks if t["agent"] in VALID_AGENTS]))
        
        if not parsed_agents:
            parsed_agents = ["fallback_agent"]
            sub_tasks = [{"agent": "fallback_agent", "task_query": question}]

        print("[DEBUG] FINAL AGENTS:", parsed_agents)
        print("[DEBUG] SUB TASKS:", sub_tasks)
        
        reasoning.append({
            "step": "supervisor",
            "message": f"Identified {len(sub_tasks)} tasks for agents: {parsed_agents}",
            "status": "success"
        })
        
        return {
            "next_agents": parsed_agents,
            "sub_tasks": sub_tasks,
            "results": {},
            "reasoning": reasoning
        }

        
    except Exception as e:
        print("\n[SUPERVISOR ERROR]", str(e))
        return {
            "next_agents": ["fallback_agent"],
            "sub_tasks": [{"agent": "fallback_agent", "task_query": state.get("question", "")}],
            "results": {},
            "reasoning": [
                f"Supervisor error: {str(e)}"
            ]
        }