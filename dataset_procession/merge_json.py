"""
合并多个JSON文件为一个JSON文件。

该模块提供了一个函数，用于将指定文件夹内所有JSON文件的内容合并为一个JSON文件。

函数说明：

- merge_json_files(input_folder_path, output_file_path)
 - input_folder_path: 需要合并的JSON文件所在的文件夹路径。
 - output_file_path: 合并后生成的新JSON文件的路径。
 - 功能: 遍历指定文件夹内的所有文件，找到后缀为'.json'的文件，逐个读取文件内容，并将内容添加到数据列表中。最后，将这个数据列表写入到指定路径的新JSON文件中。

使用示例：

```python
merge_json_files('Data/json/data_parts', 'Data/json/merged.json')
```

这将合并'Data/json/data_parts'文件夹内所有JSON文件的内容，并将合并后的数据写入'Data/json/merged.json'文件中。

依赖条件：

需要Python内置的os和json模块。
指定的输入文件夹必须存在，并且其中包含有效的JSON文件。
输出文件路径可以是新文件，也可以是覆盖现有文件。

"""
import os
import json
import sys

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
    if len(sys.argv) != 3:
        print("Usage: python merge_json.py <input_folder_path> <output_file_path>")
        sys.exit(1)

    input_folder_path = sys.argv[1]
    output_file_path = sys.argv[2]

    merge_json_files(input_folder_path, output_file_path)
