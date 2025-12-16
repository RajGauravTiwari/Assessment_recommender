from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_path=None):
        if model_path:
            self.model = SentenceTransformer(model_path)
        else:
            self.model = SentenceTransformer("all-mpnet-base-v2")

    def encode(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
