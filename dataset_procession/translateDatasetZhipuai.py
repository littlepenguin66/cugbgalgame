"""
智谱AI批量翻译JSON数据脚本。

该脚本使用智谱AI的API，提供了批量翻译JSON数据的功能。

类说明：

Translator:
翻译器类，用于处理文本翻译。
属性:
  client: 智谱AI的API客户端实例。
  model_name: 使用的模型名称。
  temperature: 翻译时的温度参数。
方法:
  translate_text: 翻译单段文本。
  translate_obj: 翻译JSON对象中的文本字段。

JSONHandler:
JSON数据处理工具类，用于从文件读取和写入JSON数据。
静态方法:
  read_json_file: 从指定路径读取JSON文件并返回数据。
  save_to_json: 将数据保存到指定路径的JSON文件。

BatchTranslator:
批量翻译器类，使用Translator实例对JSON对象进行批量翻译。
属性:
  translator: 翻译器实例。
  max_workers: 线程池的最大工作线程数。
方法:
  translate_json: 读取输入JSON文件，翻译内容，并将结果保存到输出文件。
  translate_all_files_in_folder: 遍历指定文件夹内的所有JSON文件，并翻译它们。

函数说明：

main:
脚本的入口点，负责初始化Translator和BatchTranslator实例，并开始翻译过程。

使用方法：
该脚本作为独立的Python脚本运行，需要安装智谱AI的SDK并配置API凭据。

注意：
在翻译过程中，脚本会记录错误日志到'error_log.txt'文件中。
脚本支持多线程处理，可以通过BatchTranslator的max_workers参数来设置最大线程数。
"""
import sys
import os
import json
from data_preproccessing.config_manager import config
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging
from zhipuai import ZhipuAI
from config import ZHIPUAI_API_KEY

# 设置日志记录
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Translator:
    def __init__(self, api_key, model_name="glm-4", temperature=0.8):
        self.client = ZhipuAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature

    def translate_text(self, source_text):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": f"把下文翻译成中文,并直接输出翻译后的内容,不要输出额外内容,不要出现除了翻译内容以外的东西: {source_text}"}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    def translate_obj(self, obj):
        try:
            if 'instruction' in obj:
                obj['instruction'] = self.translate_text(obj['instruction'])
            if 'input' in obj:
                obj['input'] = self.translate_text(obj['input'])
            if 'output' in obj:
                obj['output'] = self.translate_text(obj['output'])
        except Exception as e:
            logging.error(f"Error: {str(e)}, Line: {obj}")
        return obj

class JSONHandler:
    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_to_json(data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

class BatchTranslator:
    def __init__(self, translator, max_workers=5):
        self.translator = translator
        self.max_workers = max_workers

    def translate_json(self, input_file_path, output_file_path):
        data = JSONHandler.read_json_file(input_file_path)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            translated_data = list(tqdm(executor.map(self.translator.translate_obj, data), total=len(data), desc="Translating"))

        JSONHandler.save_to_json(translated_data, output_file_path)

    def translate_all_files_in_folder(self, input_folder_path, output_folder_path):
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        for file in os.listdir(input_folder_path):
            if file.endswith('.json'):
                input_file_path = os.path.join(input_folder_path, file)
                output_file_path = os.path.join(output_folder_path, 'translated_' + file)
                self.translate_json(input_file_path, output_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translateDatasetZhipuai.py <input_folder_path> <output_folder_path>")
        sys.exit(1)

    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    translator = Translator(api_key=config.ZHIPUAI_API_KEY)
    batch_translator = BatchTranslator(translator=translator)
    batch_translator.translate_all_files_in_folder(input_folder_path, output_folder_path)

