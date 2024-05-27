import json
import time
import os
import sys
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
from config import TencentCloud_SecretId, TencentCloud_SecretKey

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
    translator = Translator(secret_id=TencentCloud_SecretId, secret_key=TencentCloud_SecretKey)
    batch_translator = BatchTranslator(translator=translator)
    batch_translator.translate_json('Data/json/data_parts/part_7.json', 'Data/csv/data_zh.json')
