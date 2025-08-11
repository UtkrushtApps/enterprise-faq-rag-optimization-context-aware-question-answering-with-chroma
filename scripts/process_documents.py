import tiktoken
from sentence_transformers import SentenceTransformer
import chromadb
import os
import uuid
from pathlib import Path
import json
CHUNK_SIZE = 150
CHUNK_OVERLAP = 30
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "enterprise_faq"
model = SentenceTransformer(MODEL_NAME)
encoding = tiktoken.get_encoding('cl100k_base')
client = chromadb.HttpClient(host=os.environ.get('CHROMA_HOST', 'chroma-db'), port=8000)
coll = client.get_or_create_collection(COLLECTION_NAME)
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    tokens = encoding.encode(text)
    chunks = []
    n = len(tokens)
    start = 0
    idx = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append((chunk_text, idx, start))
        idx += 1
        start += chunk_size - overlap
    return chunks
def process_and_store_document(fpath, faq_id):
    with open(fpath, encoding='utf-8') as f:
        text = f.read()
    section = Path(fpath).stem
    meta_category = None
    if text.strip().startswith('['):
        meta_category = text.split('\n')[0].strip('[]')
    chunks = chunk_text(text)
    batch_texts = [t[0] for t in chunks]
    embeddings = model.encode(batch_texts, batch_size=8, show_progress_bar=True)
    for i, (text, idx, start_pos) in enumerate(chunks):
        meta = {
            "chunk_id": str(uuid.uuid4()),
            "faq_id": faq_id,
            "chunk_index": idx,
            "category": meta_category or "General",
            "content": text,
            "token_count": len(encoding.encode(text)),
            "title": section
        }
        coll.add(
            embeddings=[embeddings[i].tolist()],
            metadatas=[meta],
            documents=[text]
        )
def main():
    doc_dir = Path('data/documents')
    for p in doc_dir.glob("faq_*.txt"):
        process_and_store_document(str(p), p.name)
if __name__ == "__main__":
    main()
