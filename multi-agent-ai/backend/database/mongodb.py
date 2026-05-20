from pymongo import MongoClient

# =========================================================
# MONGODB CONNECTION
# =========================================================

client = MongoClient("mongodb://localhost:27017")

db = client["multi_agent_ai"]

messages_collection = db["messages"]
