# 🏦 Banking Support Chatbot

An AI-powered Banking Support Chatbot built with **Retrieval-Augmented Generation (RAG)** that answers banking-related customer queries using real document context.

## 🚀 Live Demo

> **Deployed URL:** `https://banking-chatbot-iu08.onrender.com/` 

---

## 📌 Features

- 💬 Interactive conversational chat interface
- 🧠 RAG pipeline for accurate, grounded responses
- 📄 PDF and TXT document ingestion
- 🗄️ Vector database storage using ChromaDB
- 🔍 Semantic similarity search for relevant context retrieval
- 🔁 Context retention across conversation turns
- 📤 Document upload API to expand the knowledge base
- ☁️ Deployed on Render (free tier)

---

## 🏗️ Architecture

```
User
 │
 ▼
[Chat UI - HTML/CSS/JS]
 │  POST /chat
 ▼
[FastAPI Backend - main.py]
 │
 ▼
[RAG Pipeline - rag.py]
 ├── 1. Retrieve relevant chunks from ChromaDB
 ├── 2. Build prompt with context + chat history
 └── 3. Send to Groq LLM (llama-3.3-70b)
        │
        ▼
   [ChromaDB Vector Store]
   (stores embedded banking documents)
```

---

## 🗂️ Project Structure

```
banking-chatbot/
├── main.py          # FastAPI backend with API routes
├── rag.py           # RAG pipeline (ingestion, retrieval, generation)
├── ingest.py        # One-time script to load documents into ChromaDB
├── startup.py       # Runs ingestion on server startup
├── requirements.txt # Python dependencies
├── .env             # API keys (not committed to GitHub)
├── .gitignore       # Files to exclude from Git
├── data/            # Banking documents (TXT, PDF)
│   ├── banking_faq.txt
│   └── loan_policy.txt
├── static/          # Frontend files
│   └── index.html   # Chat UI
└── uploads/         # User-uploaded documents
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Yashraj0103/banking-chatbot.git
cd banking-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at: https://console.groq.com

### 5. Ingest Banking Documents

```bash
python ingest.py
```

### 6. Start the Server

```bash
uvicorn main:app --reload
```

### 7. Open the Chatbot

Visit: `http://127.0.0.1:8000`

---

## 🔌 API Endpoints

### `GET /health`
Check if the server is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Banking chatbot is running!"
}
```

---

### `POST /chat`
Send a message and get an AI response.

**Request Body:**
```json
{
  "message": "What is a personal loan?",
  "history": []
}
```

**Response:**
```json
{
  "response": "A personal loan is an unsecured loan...",
  "status": "success"
}
```

---

### `POST /upload`
Upload a PDF or TXT document to expand the knowledge base.

**Form Data:** `file` (PDF or TXT)

**Response:**
```json
{
  "status": "success",
  "filename": "new_policy.pdf",
  "chunks_added": 12,
  "message": "Document ingested successfully (12 chunks added)"
}
```

---

## 🧠 RAG Pipeline Explanation

1. **Document Ingestion** — Banking documents (TXT/PDF) are read and split into overlapping chunks of ~500 characters
2. **Embedding Generation** — Each chunk is converted into a vector using ChromaDB's default embedding function
3. **Vector Storage** — Embeddings are stored in a local ChromaDB database
4. **Semantic Retrieval** — When a user asks a question, the top 4 most relevant chunks are retrieved using similarity search
5. **LLM Generation** — The retrieved chunks + chat history are sent to Groq's `llama-3.3-70b-versatile` model to generate a grounded response

---

## ☁️ Deployment

The application is deployed on **Render** (free tier).

- **Build Command:** `pip install -r requirements.txt && python startup.py`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variable:** `GROQ_API_KEY` set in Render dashboard

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI (Python) |
| LLM | Groq — LLaMA 3.3 70B |
| Vector DB | ChromaDB |
| Embeddings | ChromaDB Default Embedding |
| Deployment | Render |

---

## 📋 Evaluation Criteria Coverage

| Area | Implementation |
|------|---------------|
| RAG Implementation (25%) | Full pipeline in `rag.py` |
| Vector DB Usage (20%) | ChromaDB with similarity search |
| Cloud Deployment (15%) | Live on Render |
| Code Quality (15%) | Modular, commented code |
| Chatbot Accuracy (15%) | Grounded responses from documents |
| API Design (5%) | RESTful APIs with error handling |
| UI/UX (5%) | Clean chat interface |

---

## 🔮 Future Improvements

- Add streaming responses for better UX
- Implement Redis caching for faster repeated queries
- Add user authentication
- Implement reranking for better retrieval quality
- Add CI/CD pipeline with GitHub Actions
- Support DOCX file format
