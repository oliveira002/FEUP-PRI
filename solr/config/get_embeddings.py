import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()


if __name__ == "__main__":
    # Read JSON from STDIN
    #data = json.load(sys.stdin)
    file_path = 'data/filtered_games.json'

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Load JSON data from the file
        data = json.load(file)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        desc = document.get("desc", "")
        if desc is None:
            desc = ""
        full_desc = document.get("full_desc", "")
        if full_desc is None:
            full_desc = ""

        combined_text = desc + " " + full_desc
        document["vector"] = get_embedding(combined_text)

    out_file_path = 'data/semantic_games.json'
    with open(out_file_path, 'w') as file:
        # Output updated JSON to STDOUT
        json.dump(data, file, indent=2, ensure_ascii=False)
