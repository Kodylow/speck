import glob
import json
import os
import re

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

folder_path = "../bolts"
metadata_dir = "../embeddings/bolts"

# Create the metadata directory if it doesn't exist
if not os.path.exists(metadata_dir):
    os.makedirs(metadata_dir)

# Define a function to compute the number of tokens and embedding for a text


def compute_tokens_and_embedding(text):
    text = text.replace("\n", " ")
    max_length = 8191
    sections = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    embeddings = []
    tokens = 0
    for section in sections:
        embedding = get_embedding(section, model='text-embedding-ada-002')
        embeddings.append(embedding)
        tokens += len(section.split())
    return tokens, embeddings

# Define a function to get the embedding for a text using the OpenAI API


def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=[text], model=model)
    embedding = response['data'][0]['embedding']
    return embedding


for filename in glob.iglob(folder_path + "/**/*.md", recursive=True):
    with open(filename, "r") as file:
        contents = file.read()

    print(f"Processing file: {filename}")

    # Extract the sections from the contents
    sections = []
    for match in re.finditer(r"#+\s*(.+?)\n(.+?)(?=\n#+|$)", contents, re.DOTALL):
        section_dict = {}
        section_dict["header"] = match.group(1).strip()
        section_dict["text"] = match.group(2).strip()
        section_dict["length"] = len(section_dict["text"])
        section_dict["tokens"], section_dict["embedding"] = compute_tokens_and_embedding(
            section_dict["text"])
        sections.append(section_dict)

    # Create a metadata dictionary
    metadata_dict = {
        "filepath": os.path.join("bolts", os.path.relpath(filename, folder_path)),
        "sections": sections
    }

    # Create a new filename with the same name as the markdown file, but with a .json extension
    json_filename = os.path.join(metadata_dir, os.path.basename(
        os.path.splitext(filename)[0] + ".json"))

    print(f"Writing metadata to file: {json_filename}")

    # Serialize the metadata to a JSON string
    metadata_json = json.dumps(metadata_dict, indent=2)

    # Write the JSON string to the new file
    with open(json_filename, "w") as file:
        file.write(metadata_json)

print("Finished processing all files.")
