# rag.py
import os
from dotenv import load_dotenv
load_dotenv()

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from pypdf import PdfReader

# ── Setup ─────────────────────────────────────────────────────

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name="banking_docs",
    embedding_function=embedding_fn
)

# ── File Reading ──────────────────────────────────────────────

def read_file(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(
            page.extract_text() for page in reader.pages if page.extract_text()
        )
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

# ── Text Chunking ─────────────────────────────────────────────

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]

# ── Document Ingestion ────────────────────────────────────────

def ingest_documents(folder="./data"):
    files = [f for f in os.listdir(folder) if f.endswith((".txt", ".pdf"))]

    if not files:
        print("No documents found in the data folder.")
        return 0

    total = 0
    for filename in files:
        filepath = os.path.join(folder, filename)
        text = read_file(filepath)
        chunks = chunk_text(text)
        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]

        existing = collection.get(ids=ids)
        new_ids = [id for id in ids if id not in existing["ids"]]
        new_chunks = [chunks[ids.index(id)] for id in new_ids]

        if new_chunks:
            collection.add(documents=new_chunks, ids=new_ids)
            print(f"  Ingested: {filename} -> {len(new_chunks)} chunks added")
        else:
            print(f"  Skipped: {filename} already in database")

        total += len(new_chunks)

    return total

def ingest_single_file(filepath):
    filename = os.path.basename(filepath)
    text = read_file(filepath)
    chunks = chunk_text(text)
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    return len(chunks)

# ── Retrieval ─────────────────────────────────────────────────

def retrieve_context(query, top_k=4):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    chunks = results["documents"][0]
    return "\n\n---\n\n".join(chunks)

# ── Answer Generation ─────────────────────────────────────────

def get_answer(user_message, chat_history):
    context = retrieve_context(user_message)

    system_prompt = f"""You are a helpful and polite banking support assistant for an Indian bank.

RULES:
- Answer ONLY based on the context below
- If the answer is not in the context, say: "I don't have that information. Please visit your nearest branch or call our 24x7 helpline."
- Keep answers clear and concise
- Use bullet points for lists
- Always be polite and professional

CONTEXT FROM BANKING DOCUMENTS:
================================
{context}
================================"""

    # Build messages with history
    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message.content