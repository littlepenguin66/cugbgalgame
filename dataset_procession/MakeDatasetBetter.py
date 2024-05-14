import json
from tqdm.contrib.concurrent import thread_map  # 导入线程安全的tqdm函数
from zhipuai import ZhipuAI
from config import ZHIPUAI_API_KEY

# 读取json文件的函数
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 将数据保存为json文件的函数
def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

# 与ZhipuAI进行交互的函数
def interact_with_zhipuai(api_key, model_name, temperature, obj):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user",
                   "content": "把键值内的文本内容改写成问答形式,尽可能保留原有的内容，并适当做出修改，以instruction为问题，output为回答，输出时保持instruction,input和output三个属性,只要输出以下形式{instruction: "",input: "",output: [""]}" + str(
                       obj)}],
        temperature=temperature,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


# 使用多线程与ZhipuAI进行交互
def interact_with_zhipuai_multithreaded(api_key, model_name, temperature, input_file_path, output_file_path):
    data = read_json_file(input_file_path)

    # 使用tqdm.contrib.concurrent.thread_map来创建线程安全的进度条
    responses = thread_map(lambda obj: interact_with_zhipuai(api_key, model_name, temperature, obj), data, desc="Processing objects", max_workers=5)

    save_to_json(responses, output_file_path)

# 使用函数
if __name__ == "__main__":
    interact_with_zhipuai_multithreaded(ZHIPUAI_API_KEY, 'glm-3-turbo', 0.8, 'output(2).json', 'data/output1.json')