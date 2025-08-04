import os
import faiss
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer


def load_and_split_policies(policy_dir):
    chunks = []
    pattern = r"\[[^\]]+\]"
    for fname in os.listdir(policy_dir):
        if fname.endswith(".txt"):
            with open(os.path.join(policy_dir, fname), "r") as f:
                content = f.read()

                # remove all citations marks from content
                content = re.sub(pattern, "", content)

                # Simple split on triple newlines
                for part in content.split("\n\n\n"):
                    part = part.strip()
                    if part:
                        chunks.append({
                            "text": part.replace("\n", " ").replace("\u00a7", " "),
                            "source": fname.replace(".txt", "")
                        })
    print(len(chunks))
    return chunks


# # Step 1: divide into chunks & store
documents = load_and_split_policies("../policies")

with open("text_chunks.json", "w") as f:
    json.dump(documents, f)  # list of dictionaries: [{"text":..., "source":...}]


# # Step 2: create embeddings for paragraphs
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode([doc['text'] for doc in documents], convert_to_numpy=True)
print(type(embeddings))

# Step 3: build FAISS index store vector
embedding_dim = embeddings.shape[1]
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)
faiss.write_index(index, "faiss.index")


