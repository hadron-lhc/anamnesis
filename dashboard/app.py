import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data"

st.set_page_config(
    page_title="Anamnesis",
    layout="wide",
)


def header():
    st.markdown("<h1 style='text-align: left;'>Anamnesis</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")
    st.markdown(
        "<h4 style='text-align: left;'>Welcome to the Anamnesis! Here you can search and visualize medical transcriptions.</h4>",
        unsafe_allow_html=True,
    )


def main():
    header()


if __name__ == "__main__":
    main()
