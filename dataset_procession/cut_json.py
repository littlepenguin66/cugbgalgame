"""
Json Cutter - 用于分割JSON文件为多个部分的类

这个类封装了分割JSON文件的功能，提供了一个简单的接口来分割大型JSON文件。

类方法说明：
__init__(self):
- 初始化JsonCutter实例。

cut_json(self, input_file_path, output_folder_path, max_size=5000):
- 读取指定的JSON文件。
- 将JSON数据分割成多个部分，每个部分的最大大小由max_size参数指定。
- 将每个部分保存到指定输出文件夹的单独JSON文件中。

使用方法：
1. 创建JsonCutter实例。
2. 调用cut_json方法，传入输入文件路径、输出文件夹路径和可选的最大部分大小。
3. 分割后的JSON文件将被保存到指定的输出文件夹中。

注意：
- 该类依赖于json库来处理JSON数据。
- 输出文件将以'part_数字.json'的格式命名，数字从0开始。
- 如果输出文件夹不存在，将会自动创建。
"""

import json
import os
import sys

class JsonCutter:
    def __init__(self):
        pass

    def cut_json(self, input_file_path, output_folder_path, max_size=5000):
        """分割JSON文件为多个部分"""
        # 读取指定的JSON文件
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 创建输出文件夹，如果不存在
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # 分割JSON数据并保存到文件
        for i in range(0, len(data), max_size):
            part = data[i:i + max_size]
            output_file_path = os.path.join(output_folder_path, f'part_{i // max_size}.json')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(part, output_file, ensure_ascii=False, indent=4)

        print(f"JSON file split into parts and saved in {output_folder_path}")

# 使用示例
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python cut_json.py <input_json_file> <output_directory> <max_size>")
        sys.exit(1)

    input_json_file = sys.argv[1]
    output_directory = sys.argv[2]
    try:
        max_size = int(sys.argv[3])
    except ValueError:
        print("The max_size parameter should be an integer.")
        sys.exit(1)

    cutter = JsonCutter()
    cutter.cut_json(input_json_file, output_directory, max_size)
