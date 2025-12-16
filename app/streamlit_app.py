import sys
import os

# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
from recommender.scorer import SHLRecommender

DATA_PATH = "data/processed/assessments_clean.json"

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🔍 SHL Assessment Recommendation Engine")
st.write(
    "Enter a job description or hiring requirement, and get the most relevant SHL Individual Test Solutions."
)

@st.cache_resource
def load_recommender():
    return SHLRecommender(DATA_PATH)

recommender = load_recommender()

query = st.text_area(
    "Job Requirement / Description",
    height=150,
    placeholder="Example: We are hiring a software engineer with strong logical reasoning and problem-solving skills..."
)

top_k = st.slider("Number of recommendations", 5, 10, 5)

if st.button("Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a job requirement.")
    else:
        results = recommender.recommend(query, top_k=top_k)

        if not results:
            st.info("No relevant assessments found.")
        else:
            df = pd.DataFrame(results)
            df.index = df.index + 1
            df.rename(columns={
                "assessment_name": "Assessment Name",
                "url": "SHL URL",
                "score": "Relevance Score"
            }, inplace=True)

           # st.subheader("📊 Recommended Assessments")
            st.subheader("📊 Recommended Assessments")

            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "SHL URL": st.column_config.LinkColumn(
                        label="Assessment Link",
                        help="Click to open the SHL assessment page",
                        #display_text="View Assessment"
                    ),
                    "Relevance Score": st.column_config.NumberColumn(
                        format="%.4f"
                    )
                }
            )


