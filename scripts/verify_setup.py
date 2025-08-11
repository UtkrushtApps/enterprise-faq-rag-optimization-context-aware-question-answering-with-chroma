import chromadb
import os
COLLECTION_NAME = 'enterprise_faq'
client = chromadb.HttpClient(host=os.environ.get('CHROMA_HOST', 'chroma-db'), port=8000)
coll = client.get_or_create_collection(COLLECTION_NAME)
meta_count = coll.count()
print(f'Chunks in collection: {meta_count}')
sample = coll.get(limit=3)
for i, doc in enumerate(sample['documents']):
    print(f'--- Sample chunk {i+1} ---')
    print(doc[:200])
    print(sample['metadatas'][i])
