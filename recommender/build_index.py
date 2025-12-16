import json
import pandas as pd
import numpy as np
from embedding import EmbeddingModel

INPUT_PATH = "data/processed/assessments.json"
OUTPUT_EMB = "data/processed/assessment_embeddings.npy"
OUTPUT_META = "data/processed/assessments.pkl"

# -----------------------
# Load JSON safely
# -----------------------
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# If wrapped in a key, uncomment this:
# data = data["assessments"]

df = pd.DataFrame(data)

# -----------------------
# Basic validation
# -----------------------
required_cols = {"assessment_name", "description", "url"}
missing = required_cols - set(df.columns)

if missing:
    raise ValueError(f"Missing required fields: {missing}")

# -----------------------
# Clean data
# -----------------------
df = df.dropna(subset=["assessment_name", "description", "url"])
df = df.reset_index(drop=True)

# -----------------------
# Build embedding text
# -----------------------
texts = (
    df["assessment_name"].str.lower().str.strip() + ". " +
    df["description"].str.lower().str.strip()
).tolist()

# -----------------------
# Encode
# -----------------------
model = EmbeddingModel()
embeddings = model.encode(texts)

# -----------------------
# Save outputs
# -----------------------
np.save(OUTPUT_EMB, embeddings)
df.to_pickle(OUTPUT_META)

print("Embeddings saved:", embeddings.shape)
print("Metadata saved:", OUTPUT_META)
