import json
import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


directory_path = "../implementations/go/lnd"
output_directory = "../embeddings/go/lnd"

# Create the metadata directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


def compute_tokens_and_embedding(text):
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


def extract_sections(file_contents):
    sections = []
    lines = file_contents.split("\n")
    current_section = None
    for i, line in enumerate(lines):
        if line.startswith("func ") or line.startswith("type ") or (i == 0 and line.startswith("//go:build")):
            if current_section:
                current_section["content"] = "\n".join(
                    current_section["content"])
                current_section["tokens"], current_section["embedding"] = compute_tokens_and_embedding(
                    current_section["content"])
                sections.append(current_section)
            current_section = {
                "slug": line,
                "content": [line],
                "length": 0,
                "tokens": 0,
                "embedding": []
            }
        elif current_section:
            current_section["content"].append(line)
            current_section["length"] += len(line)
            current_section["tokens"] += len(line.split())
    if current_section:
        current_section["content"] = "\n".join(current_section["content"])
        current_section["tokens"], current_section["embedding"] = compute_tokens_and_embedding(
            current_section["content"])
        sections.append(current_section)
    return sections


def parse_go_file(file_path):
    try:
        with open(file_path, "r") as f:
            file_contents = f.read()
    except UnicodeDecodeError:
        print(f"Skipping file: {file_path} (not a text file)")
        return None

    if not file_path.endswith(".go"):
        print(f"Skipping file: {file_path} (not a .go file)")
        return None

    package_line_index = -1
    for i, line in enumerate(file_contents.split("\n")):
        if line.startswith("package "):
            package_line_index = i
            break
        elif i == 0 and line.startswith("//go:build"):
            for j, line2 in enumerate(file_contents.split("\n")[1:]):
                if line2.startswith("package "):
                    package_line_index = j + 1
                    break
            break

    if package_line_index == -1:
        print(f"Skipping file: {file_path} (no package declaration)")
        return None

    try:
        package_name = file_contents.split(
            "\n")[package_line_index].split(" ")[1]
    except IndexError:
        print(f"Skipping file: {file_path} (invalid package declaration)")
        return None

    sections = extract_sections(file_contents)

    output = {
        "filepath": file_path,
        "package": package_name,
        "sections": sections
    }

    return output


def write_json_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def json_has_embeddings(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        for section in data["sections"]:
            if "embedding" in section and section["embedding"]:
                return True
        return False
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False


def parse_directory(directory_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            go_file_path = os.path.join(root, file)
            output_subdirectory = os.path.join(
                output_directory, os.path.relpath(root, directory_path))
            if not os.path.exists(output_subdirectory):
                os.makedirs(output_subdirectory)
            json_file_path = os.path.join(
                output_subdirectory, file[:-2] + "json")

            if os.path.exists(json_file_path) and json_has_embeddings(json_file_path):
                print(
                    f"Skipping file: {go_file_path} (JSON file exists and has embeddings)")
            else:
                output_data = parse_go_file(go_file_path)
                if output_data is not None:
                    write_json_file(json_file_path, output_data)


parse_directory(directory_path, output_directory)
