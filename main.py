

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import books

# ── Create all database tables ───────────────
# This reads models.py and creates the "books" table in library.db
# Safe to run multiple times — only creates tables if they don't exist
Base.metadata.create_all(bind=engine)

# ── Initialize the FastAPI app ───────────────
app = FastAPI(
    title="Library Management System",
    description="A REST API to manage books — add, view, update, delete, and search.",
    version="1.0.0"
)

# ── Enable CORS ──────────────────────────────
# CORS = Cross-Origin Resource Sharing
# Without this, your browser will BLOCK requests from your HTML file
# to the FastAPI server because they are on different "origins".
# allow_origins=["*"] means allow ALL origins (fine for development).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production: replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],        # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# ── Register routes ──────────────────────────
# This connects all the /books/... endpoints we defined in routes/books.py
app.include_router(books.router)


# ── Root endpoint ────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Welcome to Library Management System API",
        "docs": "Visit /docs for interactive API documentation"
    }
