from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.routes import auth_routes, chat_routes, chat_history_routes

app = FastAPI(title="Multi-Agent AI API")

# =========================================================
# MIDDLEWARE
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTES
# =========================================================
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(chat_history_routes.router)


@app.get("/")
def read_root():
    return {"message": "Multi-Agent AI API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
