import json
import os
import re

directory_path = "../implementations/c/core-ln"
output_directory = "../embeddings/c/core-ln"

# Create the metadata directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Create a list to store the paths of skipped files
skipped_files = []


def extract_sections(file_contents, file_path):
    max_token_threshold = 1000
    num_tokens = len(file_contents.split())
    if num_tokens <= max_token_threshold:
        return [{
            "slug": file_path,
            "content": file_contents,
            "length": len(file_contents),
            "embedding": []
        }]
    sections = []
    lines = file_contents.split("\n")
    current_section = None
    for line in lines:
        if (line.startswith("struct ") or line.startswith("typedef struct ")
                or line.startswith("typedef enum ") or line.startswith("enum ")
                or line.startswith("typedef ")):
            # Extract struct or enum or typedef definition
            if current_section:
                current_section["content"] = "\n".join(
                    current_section["content"])
                sections.append(current_section)
            current_section = {
                "slug": line,
                "content": [line],
                "length": 0,
                "embedding": []
            }
        elif (re.search(r"\b(bool|short|int|long|float|double|char|void)\b", line) and
              re.search(r"\b\w+\s*\([\w\s,]*\)\s*;", line)):
            # Extract function definition
            if current_section:
                current_section["content"] = "\n".join(
                    current_section["content"])
                sections.append(current_section)
            current_section = {
                "slug": line,
                "content": [line],
                "length": 0,
                "embedding": []
            }
        elif (re.search(r"\bstatic\s+(?=bool|short|int|long|float|double|char)\b(bool|short|int|long|float|double|char)\s+\*?\w+\s*(\[[^]]*\])*\s*;", line)
              or re.search(r"^\s*\}\s*\w+\s*;", line)):
            # Extract struct or function definition
            if current_section:
                current_section["content"] = "\n".join(
                    current_section["content"])
                sections.append(current_section)
            current_section = {
                "slug": line,
                "content": [line],
                "length": 0,
                "embedding": []
            }
        elif current_section:
            current_section["content"].append(line)
            current_section["length"] += len(line)
    if current_section:
        current_section["content"] = "\n".join(current_section["content"])
        sections.append(current_section)
    if not sections:
        num_sections = (num_tokens // max_token_threshold) + 1
        section_length = len(file_contents) // num_sections
        for i in range(num_sections):
            start = i * section_length
            end = (i + 1) * section_length
            if i == num_sections - 1:
                end = len(file_contents)
            section_content = file_contents[start:end]
            sections.append({
                "slug": file_path,
                "content": section_content,
                "length": len(section_content),
                "embedding": []
            })
    return sections



def parse_c_file(file_path):
    try:
        with open(file_path, "r") as f:
            file_contents = f.read()
    except UnicodeDecodeError:
        print(f"Skipping file: {file_path} (not a text file)")

        return None

    if not (file_path.endswith(".c") or file_path.endswith(".h")):
        print(f"Skipping file: {file_path} (not a .c or .h file)")
        return None

    sections = extract_sections(file_contents, file_path)
    if not sections:
        skipped_files.append(file_path)
        print(f"No sections found in file: {file_path}")
        raise SystemExit(1)

    output = {
        "filepath": file_path,
        "sections": sections
    }

    return output


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
            c_file_path = os.path.join(root, file)
            output_subdirectory = os.path.join(
                output_directory, os.path.relpath(root, directory_path))
            if not os.path.exists(output_subdirectory):
                os.makedirs(output_subdirectory)
            if file.endswith(".h"):
                json_file_path = os.path.join(
                    output_subdirectory, file.split('.')[0] + "_h.json")
            elif file.endswith(".c"):
                json_file_path = os.path.join(
                    output_subdirectory, file.split('.')[0] + "_c.json")
            else:
                continue

            if os.path.exists(json_file_path) and json_has_embeddings(json_file_path):
                print(
                    f"Skipping file: {c_file_path} (JSON file exists and has embeddings)")
            else:
                output_data = parse_c_file(c_file_path)
                if output_data is not None:
                    write_json_file(json_file_path, output_data)


def write_json_file(file_path, data):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    if file_path.endswith(".h"):
        file_name += "_h"
    elif file_path.endswith(".c"):
        file_name += "_c"
    file_name += ".json"
    file_path = os.path.join(os.path.dirname(file_path), file_name)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


parse_directory(directory_path, output_directory)
print("Skipped files no sections:")
for file in skipped_files:
    print(file)
