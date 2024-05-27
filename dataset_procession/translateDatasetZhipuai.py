import sys
import os
import json
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

    def translate_all_files_in_folder(self, folder_path):
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                input_file_path = os.path.join(folder_path, file)
                output_file_path = os.path.join(folder_path, 'translated_' + file)
                self.translate_json(input_file_path, output_file_path)

if __name__ == "__main__":
    translator = Translator(api_key=ZHIPUAI_API_KEY)
    batch_translator = BatchTranslator(translator=translator)
    batch_translator.translate_all_files_in_folder('Data/json')
