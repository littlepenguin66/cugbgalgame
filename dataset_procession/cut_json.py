import json
import os

def cut_json(input_file_path, output_folder_path, max_size=5000):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for i in range(0, len(data), max_size):
        part = data[i:i+max_size]
        output_file_path = os.path.join(output_folder_path, f'part_{i//max_size}.json')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(part, output_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    cut_json('Data/json/geo_clean.json', 'Data/json/data_parts')