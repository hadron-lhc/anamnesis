from sentence_transformers import SentenceTransformer
from pathlib import Path
import numpy as np

DATA_PATH = Path(__file__).parent.parent / "data"
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model


def get_or_build_index(df, model=None):
    embeddings_path = DATA_PATH / "embeddings.npy"

    if embeddings_path.exists():
        embeddings = np.load(embeddings_path)
    else:
        if model is None:
            model = get_model()
        embeddings = model.encode(df["description"].tolist(), show_progress_bar=False)

    return {
        "embeddings": embeddings,
        "documents": df["description"].tolist(),
        "metadatas": [
            {
                "specialty": row["medical_specialty"].strip(),
                "sample_name": row["sample_name"].strip(),
            }
            for _, row in df.iterrows()
        ],
        "ids": [str(i) for i in range(len(df))],
    }


def search(collection, query, n=5, specialty=None):
    model = get_model()
    query_embedding = model.encode([query])[0]

    embeddings = collection["embeddings"]

    indices = list(range(len(embeddings)))
    if specialty:
        indices = [
            i for i in indices if collection["metadatas"][i]["specialty"] == specialty
        ]

    if not indices:
        return []

    subset = embeddings[list(indices)]
    norms = np.linalg.norm(subset, axis=1, keepdims=True)
    subset_norm = subset / np.clip(norms, 1e-10, None)
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    similarities = subset_norm @ query_norm

    top_n = np.argsort(similarities)[::-1][:n]

    return [
        {
            "id": collection["ids"][list(indices)[i]],
            "document": collection["documents"][list(indices)[i]],
            "specialty": collection["metadatas"][list(indices)[i]]["specialty"],
            "distance": float(1 - similarities[i]),
        }
        for i in top_n
    ]
