import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SHLRecommender:
    """
    SHL Assessment Recommender using precomputed Sentence Transformer embeddings + FAISS
    """

    def __init__(self, json_path: str):
        # -------------------------
        # Load assessment metadata
        # -------------------------
        with open(json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        # -------------------------
        # Load precomputed embeddings
        # -------------------------
        self.embeddings = np.load(
            "data/processed/assessment_embeddings.npy"
        ).astype("float32")

        # -------------------------
        # Load embedding model (query only)
        # -------------------------
        self.model = SentenceTransformer("all-mpnet-base-v2")

        # -------------------------
        # Build FAISS index
        # -------------------------
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def recommend(self, query: str, top_k: int = 5):
        if not query or not query.strip():
            return []

        # -------------------------
        # Encode query ONLY
        # -------------------------
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        # -------------------------
        # Search FAISS index
        # -------------------------
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            item = self.data[idx]
            results.append({
                "assessment_name": item["assessment_name"],
                "url": item["url"],
                "score": float(score)
            })

        return results
