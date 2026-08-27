import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import documents
from app.routes import search
from app.routes import chat


app = FastAPI(
    title="Personal RAG API"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://personal-rag-lemon.vercel.app"
).rstrip("/")


allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    FRONTEND_URL,
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(documents.router)
app.include_router(search.router)
app.include_router(chat.router)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Personal RAG API is running."
    }


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }