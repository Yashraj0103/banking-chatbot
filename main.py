# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, shutil
from rag import get_answer, ingest_single_file

app = FastAPI(title="Banking Support Chatbot API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request model ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: list = []

# ── Routes ────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Banking chatbot is running!"}


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Accepts a user message + chat history.
    Returns the AI-generated response.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    try:
        answer = get_answer(request.message, request.history)
        return {"response": answer, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or TXT file to expand the knowledge base."""
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = ingest_single_file(save_path)
    return {
        "status": "success",
        "filename": file.filename,
        "chunks_added": chunks,
        "message": f"Document ingested successfully ({chunks} chunks added)"
    }


# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")