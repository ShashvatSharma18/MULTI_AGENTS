from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.chat_service import (

    create_chat,
    save_message,
    get_user_chats,
    get_chat,
    update_chat_title,
    delete_chat
)

from backend.utils.auth_middleware import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/history", tags=["History"])

@router.delete("/delete/{chat_id}")
def remove_chat(chat_id: str, user=Depends(get_current_user)):
    success = delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}


class CreateChatRequest(BaseModel):
    user_email: str
    title: str = "New Chat"

class MessageRequest(BaseModel):
    chat_id: str
    role: str
    content: str

@router.post("/create")
def create_new_chat(data: CreateChatRequest, user=Depends(get_current_user)):
    chat_id = create_chat(
        data.user_email,
        data.title
    )
    return {"chat_id": chat_id}

@router.post("/message")
def add_message(data: MessageRequest, user=Depends(get_current_user)):
    save_message(
        data.chat_id,
        data.role,
        data.content
    )
    
    # Auto-update title if it's the first user message
    chat = get_chat(data.chat_id)
    if chat and chat.get("title") == "New Chat" and data.role == "user":
        new_title = data.content[:30] + ("..." if len(data.content) > 30 else "")
        update_chat_title(data.chat_id, new_title)
        
    return {"message": "saved"}


@router.get("/user/{user_email}")
def fetch_user_chats(user_email: str, user=Depends(get_current_user)):
    return get_user_chats(user_email)

@router.get("/{chat_id}")
def fetch_chat(chat_id: str, user=Depends(get_current_user)):
    return get_chat(chat_id)
