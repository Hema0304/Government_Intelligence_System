from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

# Load once
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def is_relevant(query, policies, threshold=0.3):
    query_vec = embeddings.embed_query(query)

    for p in policies:
        text = f"{p['name']} {p['category']} {p['benefits']} {p['target']}"
        policy_vec = embeddings.embed_query(text)

        score = cosine_similarity(query_vec, policy_vec)

        if score > threshold:
            return True

    return False