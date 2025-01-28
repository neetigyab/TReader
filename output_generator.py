import json

def save_to_json(mapped_data, output_path):
    """Save the mapped data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(mapped_data, json_file, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_path}")