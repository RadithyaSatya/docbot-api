import json
import os
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")
PATH_EMBEDDING = "data/embedding"

def embed_chunks(chunks: list[str])->list[list[float]]:
    return model.encode(chunks, convert_to_numpy=True).tolist()

def embed_query(query:str)->list[float]:
    return model.encode([query])[0].tolist()

def save_embedding(doc_id: int, chunks:list[str], embeddings:list[list[float]]):
    os.makedirs(PATH_EMBEDDING,exist_ok=True)
    data = [
        {
            "text":chunk,
            "embedding":vec
        }
        for chunk, vec in zip(chunks, embeddings)
    ]
    with open(f"{PATH_EMBEDDING}/{doc_id}.json","w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False,indent=2)

def delete_embedding(doc_id:int):
    file_path = os.path.join(PATH_EMBEDDING, doc_id)
    if os.path.exists(file_path):
        os.remove(file_path)
    