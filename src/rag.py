from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from pathlib import Path
from embeddings import search, get_or_build_index
import pandas as pd
from groq import Groq


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

DATA_PATH = Path(__file__).parent.parent / "data"


def build_prompt(question, context_docs):
    cases = ""
    for i, doc in enumerate(context_docs):
        cases += f"Case {i + 1}: {doc['document']}\n"
    prompt = f"""
        You are a medical assistant analyzing clinical transcriptions.
        Answer the question based ONLY on the following clinical cases.
        Do not use any external knowledge. If the answer is not in the
        cases, say "I don't have enough information".

        Clinical cases: {cases}

        Question: {question}

        Answer:
    """
    return prompt


def ask(collection, question, n_context=5):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    docs = search(collection, question)
    prompt = build_prompt(question, docs)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    answer = response.choices[0].message.content

    return answer


def main():
    question = "What are the most common symptoms in cardiovascular patients?"
    df = pd.read_csv(DATA_PATH / "processed.csv")
    collection = get_or_build_index(df)
    answer = ask(collection, question)
    print(answer)


if __name__ == "__main__":
    main()
