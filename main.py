from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes.books import router as books_router
import models
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)

os.makedirs("images", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/pdfs", StaticFiles(directory="pdfs"), name="pdfs")

@app.get("/")
def root():
    return {"message": "Library API Running!"}