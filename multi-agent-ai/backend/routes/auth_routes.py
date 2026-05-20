from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import BaseModel, EmailStr
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from backend.utils.jwt_handler import create_access_token
from passlib.context import CryptContext

load_dotenv()

# =========================================================
# CONFIG
# =========================================================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["multi_agent_ai"]
users_collection = db["users"]

router = APIRouter(prefix="/auth", tags=["Auth"])

# =========================================================
# MODELS & HELPERS
# =========================================================
class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# =========================================================
# ROUTES
# =========================================================

@router.post("/signup")
def signup(user: UserSignup):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pwd = hash_password(user.password)
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_pwd,
        "created_at": datetime.utcnow()
    })
    
    token = create_access_token({"email": user.email})
    return {
        "message": "Signup successful",
        "token": token,
        "email": user.email
    }

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = create_access_token({"email": user.email})
    return {
        "message": "Login successful",
        "token": token,
        "email": user.email
    }

