import sys
import os
import json
import concurrent.futures
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')


def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()


def process_document(document):
    desc = document.get("desc", "")
    if desc is None:
        desc = ""
    full_desc = document.get("full_desc", "")
    if full_desc is None:
        full_desc = ""

    combined_text = desc + " " + full_desc
    document["vector"] = get_embedding(combined_text)
    return document


if __name__ == "__main__":
    file_path = 'data/filtered_games.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    num_processes = os.cpu_count()

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        processed_data = list(executor.map(process_document, data))

    out_file_path = 'data/semantic_games.json'
    with open(out_file_path, 'w') as file:
        json.dump(processed_data, file, indent=2, ensure_ascii=False)
