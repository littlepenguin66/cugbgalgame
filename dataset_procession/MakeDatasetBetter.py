"""
本脚本旨在利用ZhipuAI API将JSON文件中的文本内容转换为问答格式。通过定义一个处理JSON文件的工具类、一个与ZhipuAI API交互的客户端类以及一个批量处理数据的类来实现。

类和函数说明：

- JSONHandler：用于读写JSON文件的工具类。
- read_json_file(file_path)：读取指定路径的JSON文件，并将其解析为Python对象。
- save_to_json(data, file_path)：将Python对象格式化为JSON格式，并保存到指定路径。

- ZhipuAIClient：封装了与ZhipuAI API交互的客户端类。
- __init__(api_key, model_name, temperature)：使用API密钥、模型名称和温度参数初始化客户端。
- interact(obj)：向ZhipuAI API发送一个包含文本对象的提示，并将其转换为问答对，返回API的响应。

- BatchProcessor：用于并行处理数据的批量处理器类。
- __init__(client, max_workers=5)：使用ZhipuAIClient实例和最大工作线程数初始化批量处理器。
- process(data)：并行处理数据列表，通过调用ZhipuAIClient的interact方法。

- main(api_key, model_name, temperature, input_file_path, output_file_path)：
主函数，负责协调整个处理流程：读取输入文件、初始化ZhipuAIClient、通过BatchProcessor处理数据，并将结果保存到输出文件。

使用方法：
运行脚本时，需要提供ZhipuAI API密钥、模型名称、温度设置、输入文件路径和输出文件路径作为参数。

依赖条件：
- 必须安装'zhipuai'模块以提供ZhipuAI API客户端。
- 'config'模块中必须定义了ZHIPUAI_API_KEY变量。
- 输入的JSON文件应包含待转换的文本内容的对象数组。
"""
import json
import sys
from data_preproccessing.config_manager import config
from tqdm.contrib.concurrent import thread_map
from zhipuai import ZhipuAI

class JSONHandler:
    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_to_json(data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

class ZhipuAIClient:
    def __init__(self, api_key, model_name, temperature):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.client = ZhipuAI(api_key=self.api_key)

    def interact(self, obj):
        prompt = (
            "把键值内的文本内容改写成问答形式,尽可能保留原有的内容，并适当做出修改，以instruction为问题，output为回答，输出时保持"
            "instruction,input和output三个属性,只要输出以下形式{instruction: \"\",input: \"\",output: [\"\"]}:" + str(obj)
        )
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

class BatchProcessor:
    def __init__(self, client, max_workers=5):
        self.client = client
        self.max_workers = max_workers

    def process(self, data):
        return thread_map(self.client.interact, data, desc="Processing objects", max_workers=self.max_workers)

def main(api_key, model_name, temperature, input_file_path, output_file_path):
    data = JSONHandler.read_json_file(input_file_path)
    client = ZhipuAIClient(api_key, model_name, temperature)
    processor = BatchProcessor(client)
    responses = processor.process(data)
    JSONHandler.save_to_json(responses, output_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python MakeDatasetBetter.py <model_name> <temperature> <input_file_path> <output_file_path>")
        sys.exit(1)

    model_name = sys.argv[2]
    temperature = float(sys.argv[3])
    input_file_path = sys.argv[4]
    output_file_path = sys.argv[5]

    main(config.ZHIPUAI_API_KEY,model_name, temperature, input_file_path, output_file_path)
