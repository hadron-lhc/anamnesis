import streamlit as st
import pandas as pd
import ast
from pathlib import Path
from embeddings import get_or_build_index, search
import sys
from custom import apply_custom_styles

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

DATA_PATH = Path(__file__).parent.parent.parent / "data"

apply_custom_styles()

st.set_page_config(page_title="Search", layout="wide")
st.title("🔍 Semantic Search")
st.markdown("Search clinical transcriptions by meaning, not just keywords.")


# Cargar datos y construir index (se cachea automáticamente en ChromaDB)
@st.cache_resource
def load_collection():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    return get_or_build_index(df)


collection = load_collection()

# Obtener especialidades únicas para el filtro
df = pd.read_csv(DATA_PATH / "processed.csv")
specialties = ["All"] + sorted(df["medical_specialty"].str.strip().unique().tolist())

# Input del usuario
query = st.text_input(
    "Search query", placeholder="e.g. patient with chest pain and hypertension"
)
specialty = st.selectbox("Filter by specialty", options=specialties)
n_results = st.slider("Number of results", min_value=1, max_value=20, value=5)

if st.button("Search") and query:
    # Pasar specialty=None si es "All"
    specialty_filter = None if specialty == "All" else specialty
    results = search(collection, query, n=n_results, specialty=specialty_filter)

    st.divider()
    for i, r in enumerate(results):
        with st.expander(
            f"Result {i + 1} — {r['specialty']} (distance: {r['distance']:.3f})"
        ):
            st.write(r["document"])
