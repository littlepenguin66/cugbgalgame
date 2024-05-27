import os
import json

def merge_json_files(input_folder_path, output_file_path):
    data = []
    files = os.listdir(input_folder_path)
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(input_folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as input_file:
                data.extend(json.load(input_file))

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    merge_json_files('Data/json/data_parts', 'Data/json/merged.json')