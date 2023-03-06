import json
import os
from uuid import uuid4

import chromadb
import openai
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

DBPATH = "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/chromadb_builder/dbs"


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai.api_key,
    model_name="text-embedding-ada-002"
)

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                  persist_directory=DBPATH))

dir_path = "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/bips"
json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

embeddings = []
documents = []
metadatas = []
ids = []

dir_path = "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/bips"
json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

for file_name in json_files:
    with open(os.path.join(dir_path, file_name), "r") as f:
        data = json.load(f)

    # get top level metadata, every key value pair except sections which I store separately
    metadata = data.copy()
    sections = metadata.pop("sections")

    for section in sections:
        section_embeddings = section["embedding"]
        for e in section_embeddings:
            metadata["length"] = section["length"]
            metadata["tokens"] = section["tokens"]
            document = section["header"] + "\n\n" + section["text"]
            embeddings.append(e)
            documents.append(document)
            metadatas.append(metadata)
            ids.append(str(uuid4()))
        del section["embedding"]

dir_path = "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/bolts"
json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

for file_name in json_files:
    with open(os.path.join(dir_path, file_name), "r") as f:
        data = json.load(f)

    # get top level metadata, every key value pair except sections which I store separately
    metadata = {"filepath": data["filepath"]}

    sections = data["sections"]
    for section in sections:
        section_embeddings = section["embedding"]
        for e in section_embeddings:
            metadata["length"] = section["length"]
            metadata["tokens"] = section["tokens"]
            document = section["header"] + "\n\n" + section["text"]
            embeddings.append(e)
            documents.append(document)
            metadatas.append(metadata.copy())
            ids.append(str(uuid4()))
        del section["embedding"]

impl_dir_paths = ["/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/go/lnd",
                  "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/c/core-ln", "/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/embeddings/rust/rust-lightning"]


def determine_doc_type(filepath):
    if "/lnd" in filepath:
        return "lnd"
    elif "/rust-lightning" in filepath:
        return "rustln"
    elif "/core-ln" in filepath:
        return "coreln"
    elif filepath.startswith("bip"):
        return "bip"
    elif filepath.startswith("bolt"):
        return "bolt"
    else:
        raise Exception("Unknown doc type")


def process_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    metadata = {"filepath": data["filepath"]}
    metadata["doc_type"] = determine_doc_type(data["filepath"])

    sections = data["sections"]
    for section in sections:
        section_embeddings = section["embedding"]
        for e in section_embeddings:
            metadata["length"] = section["length"]
            metadata["slug"] = section["slug"]
            document = section["slug"] + "\n\n" + section["content"]
            embeddings.append(e)
            documents.append(document)
            metadatas.append(metadata.copy())
            ids.append(str(uuid4()))
        del section["embedding"]


def process_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                process_file(file_path)


for impl_dir_path in impl_dir_paths:
    process_dir(impl_dir_path)
bitcoin = client.create_collection("bitcoin10", embedding_function=openai_ef)

bitcoin.add(
    embeddings=embeddings,
    metadatas=metadatas,
    documents=documents,
    ids=ids,
)

print(bitcoin.count())
