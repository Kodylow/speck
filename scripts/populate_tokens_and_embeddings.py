import json
import os
from typing import List, Tuple

import openai

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")


def compute_tokens_and_embedding(text: str) -> Tuple[int, List[float]]:
    text = text.replace("\n", " ")
    max_length = 8191
    sections = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    embeddings = []
    tokens = 0
    for section in sections:
        response = openai.Embedding.create(
            input=[section], model='text-embedding-ada-002')
        embedding = response['data'][0]['embedding']
        embeddings.append(embedding)
        tokens += len(section.split())
    return tokens, embeddings


def process_file(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        tokens_embedded = True
        for section in data["sections"]:
            if not section.get("embedding", False):
                tokens_embedded = False
                break
        if tokens_embedded:
            print(
                f"Skipping file: {json_file_path} (tokens and embeddings already exist)")
            return
        print(f"Processing file: {json_file_path}")
        for section in data["sections"]:
            if not section.get("embedding", False):
                tokens, embeddings = compute_tokens_and_embedding(
                    section["content"])
                section["tokens"] = tokens
                section["embedding"] = embeddings
        with open(json_file_path, "w") as f:
            json.dump(data, f, indent=2)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print(f"Skipping file: {json_file_path} (unable to process)")


def process_directory(directory_path: str) -> None:
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if not file.endswith(".json"):
                continue
            json_path = os.path.join(root, file)
            process_file(json_path)


if __name__ == "__main__":
    directory_path = "../embeddings/rust/rust-lightning"
    process_directory(directory_path)
