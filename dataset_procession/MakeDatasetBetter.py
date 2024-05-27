import json
from tqdm.contrib.concurrent import thread_map
from zhipuai import ZhipuAI
from config import ZHIPUAI_API_KEY

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
    main(ZHIPUAI_API_KEY, 'glm-3-turbo', 0.8, 'output(2).json', 'data/output1.json')
