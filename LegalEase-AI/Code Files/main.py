from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8501","http://127.0.0.1:8501"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def home():
    return {"message":"Welcome to LegalEase AI Legal Document Generator API"}

@app.get("/health")
def health():
    return {"status":"ok"}
