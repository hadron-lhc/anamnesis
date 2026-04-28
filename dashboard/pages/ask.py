import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from embeddings import get_or_build_index
from rag import ask
from custom import apply_custom_styles


DATA_PATH = Path(__file__).parent.parent.parent / "data"

apply_custom_styles()

st.set_page_config(page_title="Ask Assistant", layout="wide")
st.title("🤖 Medical Assistant")
st.markdown(
    "Ask questions about the clinical cases. Answers are based only on real transcriptions."
)

# Aviso importante — el modelo responde basado en datos reales
st.warning(
    "⚠️ This tool is for research purposes only and does not constitute medical advice."
)


@st.cache_resource
def load_collection():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    return get_or_build_index(df)


collection = load_collection()

# Input
question = st.text_area(
    "Your question",
    placeholder="e.g. What are the most common symptoms in cardiovascular patients?",
)
n_context = st.slider(
    "Number of cases to use as context", min_value=3, max_value=10, value=5
)

if st.button("Ask") and question:
    with st.spinner("Searching cases and generating answer..."):
        answer = ask(collection, question, n_context=n_context)
    st.divider()
    st.markdown("### Answer")
    st.write(answer)
