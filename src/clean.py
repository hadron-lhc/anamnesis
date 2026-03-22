from pathlib import Path

from exploration import load_data

DATA_PATH = Path(__file__).parent.parent / "data"


def clean_data(df):
    df_clean = df.copy()

    df_clean = df_clean.dropna(subset=["transcription"])
    df_clean = df_clean.drop(columns=["Unnamed: 0"])

    return df_clean


def main():
    df = load_data()
    df_clean = clean_data(df)
    df_clean.to_csv(DATA_PATH / "clean.csv", index=False)
    print("Guardado en data/clean.csv")


if __name__ == "__main__":
    main()
