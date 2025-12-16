##Link : https://shl-assessment-recommender-raj.streamlit.app/
# SHL Assessment Recommendation System

An intelligent recommendation system that suggests relevant SHL Individual Test Solutions based on natural language hiring queries or job descriptions using semantic search and transformer-based embeddings.

## Overview

This project implements a production-grade semantic recommendation system that:
- Uses the official SHL Product Catalog as the source of truth
- Recommends 5-10 relevant individual test solutions for any hiring query
- Excludes pre-packaged job solutions
- Leverages modern retrieval-based techniques for semantic matching
- Provides results in a clear, tabular format with assessment URLs

## Architecture

```
User Query → Sentence Transformer → FAISS Vector Search → Top-K Matches → Tabular Results
```

The system consists of four main components:

1. **Data Ingestion Pipeline** - Web scraping and parsing
2. **Data Processing** - Normalization and structuring
3. **Embedding & Indexing** - Semantic representation using transformers
4. **Query & Retrieval** - Real-time similarity search

## Data Source

The system uses the official SHL Product Catalog:
```
https://www.shl.com/products/product-catalog/
```

**Dataset Statistics:**
- 517 individual test solutions
- 526+ unique assessment pages discovered
- 100% sourced from canonical SHL catalog

## Technology Stack

- **Python** - Core implementation language
- **requests** - HTTP client for web scraping
- **BeautifulSoup** - HTML parsing
- **Sentence Transformers** - Semantic embeddings (`all-mpnet-base-v2`)
- **FAISS** - Efficient vector similarity search
- **NumPy** - Numerical operations

## Web Scraping Strategy

### Pagination Handling
The crawler navigates the SHL catalog using query-based pagination:
```
/products/product-catalog/?start=0&type=1
/products/product-catalog/?start=12&type=1
```

- Iterates through `start` offsets and catalog types
- Automatically terminates when no new links are found
- Discovers 526+ unique assessment URLs

### Link Discovery
- Extracts all anchor tags from catalog pages
- Filters for assessment detail URLs
- Uses set-based de-duplication to ensure each assessment is visited once

### Content Extraction
From each assessment page, the system extracts:
- Assessment name
- Assessment description (from structured sections or main content)
- Canonical SHL product URL

## Key Challenges & Solutions

### 1. URL Aliasing
**Challenge:** Same assessment accessible via multiple URL patterns
```
/products/product-catalog/view/python-new/
/solutions/products/product-catalog/view/python-new/
```
**Solution:** Normalized all URLs to canonical `/products/product-catalog/` format

### 2. Excluding Pre-packaged Solutions
**Challenge:** Catalog contains both individual tests and job solution bundles

**Solution:** Page-level text analysis identifies and excludes content marked as "job solution" or "pre-packaged"

### 3. Inconsistent Page Structures
**Challenge:** Assessment pages lack uniform HTML structure

**Solution:** Hierarchical fallback-based parsing strategy with multiple extraction patterns

### 4. Rate Limiting
**Challenge:** Aggressive crawling risks timeouts

**Solution:** Introduced request delays and graceful error handling

## Data Processing

### Structured Representation
```json
{
  "assessment_name": "Python Coding Assessment",
  "description": "Evaluates programming skills...",
  "url": "https://www.shl.com/products/product-catalog/view/python-new/"
}
```

### Normalization Steps
1. Lowercasing all text
2. Removing excess whitespace
3. Normalizing line breaks
4. Concatenating name and description into semantic units

## Embedding & Indexing

### Model Choice
**Sentence Transformer:** `all-mpnet-base-v2`
- High-quality 768-dimensional embeddings
- Captures semantic similarity beyond keyword matching
- No fine-tuning required

### Offline Processing
Generated artifacts:
- `assessment_embeddings.npy` - NumPy array (N × 768)
- Assessment metadata (JSON/PKL) - Index-to-assessment mapping

### Vector Index
- **FAISS IndexFlatIP** with normalized vectors
- Inner product similarity ≈ cosine similarity
- Enables efficient nearest-neighbor search

## Query Processing

### Runtime Flow
1. Encode user query using Sentence Transformer
2. Normalize query embedding to unit length
3. Perform FAISS similarity search
4. Map result indices to assessment metadata
5. Return top-K recommendations with scores

### Output Format
```
| Rank | Assessment Name              | SHL URL                          | Score |
|------|------------------------------|----------------------------------|-------|
| 1    | Python Coding Assessment     | https://www.shl.com/...          | 0.89  |
| 2    | Software Development Test    | https://www.shl.com/...          | 0.85  |
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd shl-recommendation-system

# Install dependencies
pip install -r requirements.txt
```

### Required Libraries
```
requests
beautifulsoup4
sentence-transformers
faiss-cpu  # or faiss-gpu
numpy
```

## Usage

### Running the Scraper
```python
python scraper.py
```

### Generating Embeddings
```python
python generate_embeddings.py
```

### Making Recommendations
```python
from recommender import SHLRecommender

recommender = SHLRecommender()
results = recommender.recommend("Looking for a Python developer", top_k=5)
print(results)
```

## Evaluation

The system is designed for evaluation using standard information retrieval metrics:

- **Precision@K** - Proportion of relevant assessments in top-K results
- **Recall@K** - Coverage of relevant assessments
- **MAP** - Mean Average Precision across queries
- **NDCG** - Normalized Discounted Cumulative Gain

## Project Structure

```
shl-assessment-recommender/
│
|── api/
│   └── main.py
│       # API Endpoints.
|
├── app/
│   └── streamlit_app.py
│       # Streamlit UI: takes user query, calls recommender, displays Top-5/10 results
│
├── crawler/
│   ├── crawl_catalog.py
│   │   # Crawls SHL Product Catalog pages and discovers assessment URLs
│   │
│   ├── parse_assessment.py
│   │   # Visits each assessment URL and extracts name, description, canonical URL
│   │
│   ├── test_requests.py
│   │   # Utility script to test HTTP requests and page responses
│   │
│   └── __init__.py
│       # Marks crawler as a Python package
│
├── recommender/
│   ├── build_index.py
│   │   # One-time offline script to generate sentence embeddings for all assessments
│   │
│   ├── scorer.py
│   │   # Core recommendation logic: loads embeddings, builds FAISS index,
│   │   # encodes query, retrieves Top-K matching assessments
│   │
│   └── __init__.py
│       # Marks recommender as a Python package
│
├── data/
│   ├── raw/
│   │   └── shl_catalog_raw.json
│   │       # Raw scraped data directly from SHL Product Catalog (before cleaning)
│   │
│   └── processed/
│       ├── assessments_clean.json
│       │   # Cleaned, deduplicated assessment metadata used by the recommender
│       │
│       ├── assessment_embeddings.npy
│       │   # Precomputed sentence embeddings for all assessments (trained artifact)
│       │
│       └── assessments.pkl
│           # Serialized assessment metadata aligned with embedding indices
│
├── notebooks/
│   └── exploration.ipynb
│       # Optional notebook for exploratory analysis and sanity checks
│
├── requirements.txt
│   # Python dependencies required to run scraping, embedding, and UI
│
├── README.md
│   # Complete project documentation (Sections 1–14)
│
├── .gitignore
│   # Excludes virtual environment, cache files, and raw artifacts from Git
│
└── venv/
    # Local virtual environment (not committed to version control)

```

## Features

✅ Semantic search beyond keyword matching  
✅ Scalable vector similarity search  
✅ Deterministic, reproducible results  
✅ Evaluation-ready architecture  
✅ Clean separation of concerns  
✅ Production-grade error handling  

## Future Enhancements

- Fine-tune embeddings on hiring domain data
- Implement query expansion techniques
- Add hybrid search (semantic + keyword)
- Support for multi-modal inputs (job descriptions + requirements)
- Real-time catalog updates
- A/B testing framework for model improvements

## Contact
Raj Gaurav Tiwari
rajt4656@gmail.com



---

**Note:** This system is designed for research and evaluation purposes. Ensure compliance with SHL's terms of service when scraping their catalog.
