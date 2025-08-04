import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# load both text & embeddings
index = faiss.read_index("faiss.index")
with open("text_chunks.json", "r") as f:
    text_chunks = json.load(f)

# Step 4: define the search function
def semantic_search(query: str, top_k: int=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [(text_chunks[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return results



revised_question = "What is notability?"
results = semantic_search(revised_question)

print("Top relevant chunks:")
for text, score in results:
    print(f"- {text} (Score: {score:.4f})")
