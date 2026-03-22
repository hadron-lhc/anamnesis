from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data"


def load_data():
    """Load the MTSamples dataset from the CSV file."""
    df = pd.read_csv(DATA_PATH / "mtsamples.csv")
    return df


def main():
    df = load_data()
    # Especialidades médicas disponibles
    print(df["medical_specialty"].value_counts().head(20))
    print()
    # Longitud de las transcripciones
    df["text_length"] = df["transcription"].str.len()
    print(df["text_length"].describe())
    print()
    # Valores nulos
    print(df.isnull().sum())


if __name__ == "__main__":
    main()
