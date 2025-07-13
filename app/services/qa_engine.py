import json

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
from app.services.embedder import embed_query


def load_embedding(doc_id:int):
    with open(f"data/embedding/{doc_id}.json","r",encoding="utf-8") as f:
        return json.load(f)
    
def find_most_relevant_chunk(query:str, doc_id:int)-> str:
    chunks = load_embedding(doc_id)
    query_embedding = embed_query(query)

    chunk_embeddings= np.array([chunk["embedding"] for chunk in chunks])
    sims = cosine_similarity([query_embedding], chunk_embeddings)[0]
    best_idx = int(np.argmax(sims))

    return chunks[best_idx]["text"]
    