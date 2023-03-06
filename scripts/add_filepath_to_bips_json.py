import os
import json

metadata_dir = "../embeddings/bips"

for filename in os.listdir(metadata_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(metadata_dir, filename)
        with open(file_path, "r+") as file:
            data = json.load(file)
            data["filepath"] = f"bips/{filename[:-5]}.mediawiki"
            file.seek(0)
            json.dump(data, file, indent=2)
            file.truncate()
