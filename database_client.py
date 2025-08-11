import chromadb
import json
from typing import List
from pathlib import Path

def get_db_config():
    db_conf = Path('config/database.json')
    with open(db_conf) as f:
        cfg = json.load(f)
    return cfg['host'], cfg['port'], cfg['collection']

def get_chroma_collection():
    host, port, collection = get_db_config()
    client = chromadb.HttpClient(host=host, port=port)
    return client.get_or_create_collection(collection)

def query_chunks(vector: List[float], top_k: int = 5):
    coll = get_chroma_collection()
    return coll.query(query_embeddings=[vector], n_results=top_k)
