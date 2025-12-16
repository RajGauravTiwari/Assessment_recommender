import os
from fastapi import FastAPI
from pydantic import BaseModel
from recommender.scorer import SHLRecommender

# ============================================================
# Resolve project root directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "assessments.json"
)

# ============================================================
# Initialize FastAPI application
# ============================================================
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API that recommends relevant SHL Individual Test Solutions based on a natural language query",
    version="1.0.0"
)

# ============================================================
# Load recommender once at startup
# (Uses precomputed embeddings + FAISS index)
# ============================================================
recommender = SHLRecommender(json_path=DATA_PATH)

# ============================================================
# Request schema
# ============================================================
class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

# ============================================================
# Health Check Endpoint
# ============================================================
@app.get("/health")
def health_check():
    """
    Simple health check endpoint to verify the API is running.
    """
    return {
        "status": "ok",
        "message": "SHL Assessment Recommendation API is running"
    }

# ============================================================
# Assessment Recommendation Endpoint
# ============================================================
@app.post("/recommend")
def recommend_assessments(request: RecommendationRequest):
    """
    Accepts a job description or natural language query and returns
    1–10 relevant SHL Individual Test Solutions.
    """

    # Enforce min = 1, max = 10
    top_k = min(max(request.top_k, 1), 10)

    results = recommender.recommend(
        query=request.query,
        top_k=top_k
    )

    recommended_assessments = []

    for item in results:
        recommended_assessments.append({
            "url": item["url"],
            "name": item["assessment_name"],
            "adaptive_support": item.get("adaptive_support", "No"),
            "description": item.get("description", ""),
            "duration": item.get("duration", None),
            "remote_support": item.get("remote_support", "Yes"),
            "test_type": item.get("test_type", [])
        })

    return {
        "recommended_assessments": recommended_assessments
    }
