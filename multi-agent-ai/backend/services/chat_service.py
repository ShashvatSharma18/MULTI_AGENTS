from datetime import datetime
from bson import ObjectId
from backend.database.chat_history import chat_collection

def create_chat(user_email, title="New Chat"):
    chat = {
        "user_email": user_email,
        "title": title,
        "messages": [],
        "created_at": datetime.utcnow()
    }
    result = chat_collection.insert_one(chat)
    return str(result.inserted_id)

def save_message(chat_id, role, content):
    chat_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )

def get_user_chats(user_email):
    chats = list(
        chat_collection.find(
            {"user_email": user_email},
            {"messages": 0}
        ).sort("created_at", -1)
    )
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    return chats

def get_chat(chat_id):
    chat = chat_collection.find_one(
        {"_id": ObjectId(chat_id)}
    )
    if chat:
        chat["_id"] = str(chat["_id"])
    return chat

def update_chat_title(chat_id, title):
    chat_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {
            "$set": {
                "title": title
            }
        }
    )

def delete_chat(chat_id):
    result = chat_collection.delete_one(
        {"_id": ObjectId(chat_id)}
    )
    return result.deleted_count > 0

