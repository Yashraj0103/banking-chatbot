# ingest.py — Run this ONCE to load documents into the database
from rag import ingest_documents

print("Loading banking documents into vector database...")
count = ingest_documents("./data")
print(f"\nDone! Total chunks stored: {count}")
print("You can now start the server with: uvicorn main:app --reload")