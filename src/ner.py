from transformers import pipeline
from dotenv import load_dotenv
from exploration import load_data
from clean import clean_data
import os
import time

_ner = None


def get_ner():
    global _ner
    load_dotenv()
    os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
    if _ner is None:
        _ner = pipeline(
            "ner", model="d4data/biomedical-ner-all", aggregation_strategy="first"
        )
    return _ner


def create_entities(text):
    ner = get_ner()
    return ner(text)


def chunk_text(text, chunk_size=400, overlap=50):
    """
    Example of chunking:
        Chunk 1: "...the patient was diagnosed with type 2 diabetes"
        Chunk 2: "type 2 diabetes mellitus and prescribed..."
        Overlap: "type 2 diabetes"
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # retrocedes 'overlap' palabras
    return chunks


def extract_entities(text):
    chunks = chunk_text(text)
    all_entities = []
    for chunk in chunks:
        entities = create_entities(chunk)
        all_entities.extend(entities)

    all_entities = [
        e for e in all_entities if e["score"] > 0.85 and len(e["word"].strip()) > 2
    ]
    return all_entities


def process_dataset(df, batch_size=500, output_path="data/processed.csv"):
    results = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i : i + batch_size]
        for row in batch.itertuples():
            entities = extract_entities(row.transcription)
            results.append(entities)
        # guardar progreso después de cada batch
        df_temp = df.iloc[: len(results)].copy()
        df_temp["entities"] = results
        df_temp.to_csv(output_path, index=False)
        print(f"Procesadas {len(results)}/{len(df)} transcripciones")
    return df_temp


def main():
    """
    df = load_data()
    df_clean = clean_data(df)
    start = time.time()
    df_processed = process_dataset(df_clean)
    print(f"Proceso completo: {time.time() - start:.1f}s")
    print("Guardado en data/processed.csv")
    """

    import pandas as pd

    df = pd.read_csv("data/processed.csv")
    print(df.shape)
    print(df.columns.tolist())
    print(df["entities"].iloc[0][:200])  # primeras entidades de la primera fila


if __name__ == "__main__":
    main()
