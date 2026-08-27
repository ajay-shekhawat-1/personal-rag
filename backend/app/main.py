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

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://personal-h2u8u3qje-ajay-2382.vercel.app",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(
    documents.router
)

app.include_router(
    search.router
)

app.include_router(
    chat.router
)


@app.get("/")
def root():

    return {
        "message": "Personal RAG API is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }