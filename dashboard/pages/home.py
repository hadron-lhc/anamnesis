import streamlit as st
from pathlib import Path
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
import plotly.express as px
import ast

DATA_PATH = Path(__file__).parent.parent / "data"


st.set_page_config(
    page_title="Anamnesis",
    layout="wide",
)


def header():
    st.markdown(
        "<h1>Anamnesis</h1>",
        unsafe_allow_html=True,
    )

    add_vertical_space(2)

    st.markdown(
        "Medical transcription analytics dashboard",
    )

    add_vertical_space(2)


def parse_entities(df):
    df["entities"] = df["entities"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )

    return df


def count_unique_entities(df):
    return len(set(ent["word"] for row in df["entities"] for ent in row))


def count_total_entities(df):
    return sum(len(row) for row in df["entities"])


def show_metrics(df):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total transcriptions",
            len(df),
        )

    with col2:
        st.metric(
            "Medical specialties",
            df["medical_specialty"].nunique(),
        )

    with col3:
        st.metric(
            "Unique entities",
            count_unique_entities(df),
        )

    with col4:
        st.metric(
            "Total entities detected",
            count_total_entities(df),
        )

    with col5:
        st.metric(
            "Avg entities per transcription", round(df["entities_count"].mean(), 1)
        )


def get_chart(df):
    counts = df["medical_specialty"].value_counts().reset_index()

    fig = px.bar(
        counts,
        x="count",
        y="medical_specialty",
        labels={
            "count": "Count",
            "medical_specialty": "Medical specialty",
        },
        title="Medical specialties distribution",
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    df["entities"] = df["entities"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )
    df["entities_count"] = df["entities"].apply(len)
    return df


def main():
    df = load_data()

    header()

    show_metrics(df)

    chart = get_chart(df)

    st.plotly_chart(
        chart,
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
