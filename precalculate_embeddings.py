import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

DATA_PATH = Path("data")
df = pd.read_csv(DATA_PATH / "processed.csv")
print(f"Calculando embeddings para {len(df)} filas...")
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
embeddings = model.encode(df["description"].tolist(), show_progress_bar=True)
np.save(DATA_PATH / "embeddings.npy", embeddings)
print("✅ Listo! Archivo guardado en data/embeddings.npy")
