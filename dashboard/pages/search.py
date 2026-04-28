import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from embeddings import get_model, get_or_build_index, search
from custom import apply_custom_styles

DATA_PATH = Path(__file__).parent.parent.parent / "data"

apply_custom_styles()
st.set_page_config(page_title="Search", layout="wide")
st.title("🔍 Semantic Search")
st.markdown("Search clinical transcriptions by meaning, not just keywords.")


@st.cache_resource
def load_model():
    return get_model()


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH / "processed.csv")


@st.cache_resource
def load_collection():
    df = load_data()
    model = load_model()
    return get_or_build_index(df, model=model)


# Pre-cargar al arrancar
with st.spinner("Loading model and index... (first time only)"):
    load_model()
    collection = load_collection()

df = load_data()
specialties = ["All"] + sorted(df["medical_specialty"].str.strip().unique().tolist())

query = st.text_input(
    "Search query", placeholder="e.g. patient with chest pain and hypertension"
)
specialty = st.selectbox("Filter by specialty", options=specialties)
n_results = st.slider("Number of results", min_value=1, max_value=20, value=5)

if st.button("Search") and query:
    specialty_filter = None if specialty == "All" else specialty
    results = search(collection, query, n=n_results, specialty=specialty_filter)
    st.divider()
    if not results:
        st.warning("No results found for the selected filters.")
    for i, r in enumerate(results):
        with st.expander(
            f"Result {i + 1} — {r['specialty']} (distance: {r['distance']:.3f})"
        ):
            st.write(r["document"])
