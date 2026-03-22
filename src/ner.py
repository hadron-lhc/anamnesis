from transformers import pipeline
from dotenv import load_dotenv
import os


def create_entities(text):
    load_dotenv()
    os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

    ner = pipeline(
        "ner", model="d4data/biomedical-ner-all", aggregation_strategy="simple"
    )

    entities = ner(text)

    return entities


def main():
    text = "The patient has diabetes type 2 and was prescribed metformin 500mg daily."

    entities = create_entities(text)
    print(entities)


if __name__ == "__main__":
    main()
