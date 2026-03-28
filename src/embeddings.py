import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data"


def get_or_build_index(df):
    client = chromadb.PersistentClient(path=str(DATA_PATH / "chroma"))
    collection = client.get_or_create_collection("transcriptions")
    if collection.count() == 0:
        collection.add(
            documents=df["description"].tolist(),
            ids=[str(i) for i in range(len(df))],
            metadatas=[
                {
                    "specialty": row["medical_specialty"].strip(),
                    "sample_name": row["sample_name"].strip(),
                }
                for _, row in df.iterrows()
            ],
        )
    return collection


def search(collection, query, n=5, specialty=None):
    where = {"specialty": specialty} if specialty else None
    results = collection.query(query_texts=[query], n_results=n, where=where)
    output = []
    for i in range(len(results["ids"][0])):
        output.append(
            {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "specialty": results["metadatas"][0][i]["specialty"],
                "distance": results["distances"][0][i],
            }
        )
    return output


def main():
    df = pd.read_csv(DATA_PATH / "processed.csv")
    collection = get_or_build_index(df)
    query_texts = "patient with chest pain"
    specialty_name = "Cardiovascular / Pulmonary"
    result = search(collection, query_texts, specialty=specialty_name)
    print(result)


if __name__ == "__main__":
    main()
