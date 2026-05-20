from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.graph.builder import graph
from backend.utils.auth_middleware import get_current_user
from typing import List, Optional
import json
import asyncio

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    resume_text: Optional[str] = ""
    history: List[dict] = []

async def generate_stream(request: ChatRequest, thread_id: str):
    """
    Generator that streams LangGraph events to the frontend.
    """
    inputs = {
        "question": request.message,
        "resume_text": request.resume_text,
        "messages": request.history
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # 1. Initial Status
    yield f"data: {json.dumps({'type': 'status', 'content': '🧠 Initializing Shark Engine Core...'})}\n\n"
    await asyncio.sleep(0.1)

    try:
        final_result = "Internal Engine Error: No response aggregated."
        
        # 2. Stream LangGraph Steps
        async for event in graph.astream(inputs, config=config, stream_mode="values"):
            # In 'values' mode, event is the ENTIRE state at that moment
            if "result" in event and event["result"]:
                final_result = event["result"]
            
            # Extract simple status info (we can't easily get node name in 'values' mode without complex parsing,
            # but we can check the length of reasoning)
            reasoning = event.get("reasoning", [])
            if reasoning:
                last_node = reasoning[-1].get("step", "Processing")
                last_msg = reasoning[-1].get("message", "Synthesizing...")
                yield f"data: {json.dumps({'type': 'status', 'content': f'⚙️ {last_node.title()}: {last_msg}'})}\n\n"

        # 3. Final Result Streaming
        # Clear the status and start token stream
        yield f"data: {json.dumps({'type': 'token', 'content': ''})}\n\n"
        
        # Token-by-token playback
        chunk_size = 25 
        for i in range(0, len(final_result), chunk_size):
            chunk = final_result[i:i+chunk_size]
            yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            await asyncio.sleep(0.015)



    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': f'Signal Failure: {str(e)}'})}\n\n"

@router.post("/run")
async def run_chat(request: ChatRequest, user=Depends(get_current_user)):
    thread_id = user.get("email")
    return StreamingResponse(
        generate_stream(request, thread_id),
        media_type="text/event-stream"
    )
