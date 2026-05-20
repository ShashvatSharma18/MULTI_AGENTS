from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["multi_agent_ai"]
chat_collection = db["chat_sessions"]
