import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data"


def build_index(df):
    # 1. Crear cliente y colección
    client_path = DATA_PATH / "chroma"
    client = chromadb.PersistentClient(path=client_path)
    collections = client.get_or_create_collection("transcriptions")

    # 2. Agregar documentos
    collections.add(
        documents=df["description"].tolist(),
        ids=[str(i) for i in range(len(df))],
        metadatas=[
            {"specialty": row["medical_specialty"], "sample_name": row["sample_name"]}
            for _, row in df.iterrows()
        ],
    )
    return collections


def main():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    collection = build_index(df)
    results = collection.query(query_texts=["patient with chest pain"], n_results=5)
    print(results)


if __name__ == "__main__":
    main()
