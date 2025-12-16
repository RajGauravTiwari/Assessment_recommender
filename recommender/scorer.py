import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SHLRecommender:
    def __init__(self, data_path: str):
        # Load parsed assessment data
        with open(data_path, "r", encoding="utf-8") as f:
            self.assessments = json.load(f)

        # Prepare corpus
        self.descriptions = [
            item["description"] for item in self.assessments
        ]

        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2)
        )

        # Fit TF-IDF on assessment descriptions
        self.tfidf_matrix = self.vectorizer.fit_transform(self.descriptions)

    def recommend(self, query: str, top_k: int = 10):
        """
        Recommend top_k assessments based on cosine similarity.
        """
        if not query.strip():
            return []

        # Vectorize query
        query_vector = self.vectorizer.transform([query])

        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "assessment_name": self.assessments[idx]["assessment_name"],
                "url": self.assessments[idx]["url"],
                "score": float(similarities[idx])
            })

        return results
