import streamlit as st
import pandas as pd
import plotly.express as px
import ast
from pathlib import Path
from collections import Counter
import sys
from custom import apply_custom_styles

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

DATA_PATH = Path(__file__).parent.parent.parent / "data"

apply_custom_styles()

st.set_page_config(page_title="Analytics", layout="wide")
st.title("📊 Entity Analytics")
st.markdown("Explore the most common medical entities extracted from transcriptions.")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    df["entities"] = df["entities"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )
    return df


df = load_data()

# Filtro por especialidad
specialties = ["All"] + sorted(df["medical_specialty"].str.strip().unique().tolist())
specialty = st.selectbox("Filter by specialty", specialties)

if specialty != "All":
    df = df[df["medical_specialty"].str.strip() == specialty]

# Filtro por tipo de entidad
entity_types = [
    "All",
    "Disease_disorder",
    "Medication",
    "Sign_symptom",
    "Diagnostic_procedure",
    "Biological_structure",
    "Lab_value",
]
entity_type = st.selectbox("Filter by entity type", entity_types)

# Contar entidades
all_entities = [ent for row in df["entities"] for ent in row]
if entity_type != "All":
    all_entities = [e for e in all_entities if e["entity_group"] == entity_type]

# Top 20 entidades más frecuentes
counter = Counter(e["word"] for e in all_entities)
top_entities = pd.DataFrame(counter.most_common(20), columns=["entity", "count"])

# Gráfico
fig = px.bar(
    top_entities,
    x="count",
    y="entity",
    title=f"Top 20 most common entities",
    labels={"count": "Frequency", "entity": "Entity"},
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# Distribución por tipo de entidad
st.divider()
entity_type_counts = Counter(
    e["entity_group"] for e in [ent for row in df["entities"] for ent in row]
)

df_types = pd.DataFrame(entity_type_counts.items(), columns=["type", "count"])
threshold = 2.0
df_types["type"] = df_types.apply(
    lambda row: row["type"]
    if (row["count"] / df_types["count"].sum() * 100) > threshold
    else "Other",
    axis=1,
)
df_types = df_types.groupby("type")["count"].sum().reset_index()
fig2 = px.pie(df_types, values="count", names="type", title="Entity type distribution")
fig2.update_layout(
    legend=dict(
        orientation="v",
        x=0.80,  # posición horizontal — ajustá este valor
        y=0.6,  # centrado vertical
        xanchor="left",
        yanchor="middle",
        font=dict(size=14),  # ← tamaño del texto
    ),
    margin=dict(l=0, r=200, t=40, b=0),  # r=200 da espacio para la leyenda
)
st.plotly_chart(fig2, use_container_width=True)
