"""
腾讯云批量翻译JSON数据脚本。

该脚本使用腾讯云翻译API，提供了批量翻译JSON数据的功能。

类说明：

RateLimiter:
速率限制器，用于控制每秒请求的最大数量。
属性:
   max_rate (int): 每秒允许的最大请求次数。
   count (int): 自上次一秒以来的请求次数。
   start_time (float): 第一次请求的开始时间。

Translator:
翻译器类，用于处理使用腾讯云TMT API的文本翻译。
属性:
   cred: 腾讯云API凭据。
   http_profile: HTTP配置。
   client_profile: 客户端配置。
   client: TMT客户端实例。
   limiter: 速率限制器实例。

JSONHandler:
JSON数据处理工具类，用于从文件读取和写入JSON数据。
静态方法:
   read_json_file: 从指定路径读取JSON文件并返回数据。
   save_to_json: 将数据保存到指定路径的JSON文件。

BatchTranslator:
批量翻译器类，使用Translator实例对JSON对象进行批量翻译。
方法:
   translate_obj: 翻译JSON对象中的文本字段。
   translate_json: 读取输入JSON文件，翻译内容，并将结果保存到输出文件。

函数说明：

main:
脚本的入口点，负责初始化Translator和BatchTranslator实例，并开始翻译过程。

使用方法：
该脚本作为独立的Python脚本运行，需要安装腾讯云SDK并配置API凭据。

注意：
在翻译过程中，脚本会定期保存翻译进度，以防止数据丢失。
"""
import json
import time
import os
import sys
from data_preproccessing.config_manager import config
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

class RateLimiter:
    def __init__(self, max_rate):
        self.max_rate = max_rate
        self.count = 0
        self.start_time = time.time()

    def request(self):
        time_diff = time.time() - self.start_time
        if time_diff >= 1:
            self.count = 0
            self.start_time = time.time()
        if self.count >= self.max_rate:
            time.sleep(1 - time_diff)
        self.count += 1

class Translator:
    def __init__(self, secret_id, secret_key, region="ap-beijing", max_rate=5):
        self.cred = credential.Credential(secret_id, secret_key)
        self.http_profile = HttpProfile(endpoint="tmt.tencentcloudapi.com")
        self.client_profile = ClientProfile(httpProfile=self.http_profile)
        self.client = tmt_client.TmtClient(self.cred, region, self.client_profile)
        self.limiter = RateLimiter(max_rate)

    def translate_text(self, source_text, source_lang='en', target_lang='zh'):
        for _ in range(3):  # Try up to 3 times
            try:
                req = models.TextTranslateRequest()
                req.SourceText = source_text
                req.Source = source_lang
                req.Target = target_lang
                req.ProjectId = 0

                resp = self.client.TextTranslate(req)
                model = models.TextTranslateResponse()
                model._deserialize(json.loads(resp.to_json_string()))
                self.limiter.request()  # 在请求成功后调用
                time.sleep(0.2)  # 暂停0.2秒
                return model.TargetText

            except TencentCloudSDKException as err:
                print(f"Error occurred: {err}, retrying...")
                time.sleep(1)  # Wait for a while before retrying
        return None  # Return None if all retries failed

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
    def __init__(self, translator):
        self.translator = translator

    def translate_obj(self, obj):
        if 'instruction' in obj:
            obj['instruction'] = self.translator.translate_text(obj['instruction'])
        if 'output' in obj:
            obj['output'] = self.translator.translate_text(obj['output'])
        return obj

    def translate_json(self, input_file_path, output_file_path):
        data = JSONHandler.read_json_file(input_file_path)
        total = len(data)
        for i, obj in enumerate(data, 1):
            print(f"Translating {i}/{total}...")
            obj = self.translate_obj(obj)
            if i % 100 == 0:  # 每完成100个对象就保存一次
                JSONHandler.save_to_json(data[:i], output_file_path)
        JSONHandler.save_to_json(data, output_file_path)  # 最后再保存一次，确保所有数据都被保存

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translateDatasetTencent.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    translator = Translator(secret_id=config.TencentCloud_SecretId, secret_key=config.TencentCloud_SecretKey)
    batch_translator = BatchTranslator(translator=translator)
    batch_translator.translate_json(input_file_path, output_file_path)
