# 模型下载
from modelscope import snapshot_download

model_dir = snapshot_download("ZhipuAI/chatglm3-6b", revision = "v1.0.0", cache_dir='.\models')

"""
model_id = {'baicai003/Phi-3-mini-128k-instruct-Chinese',
            'LLM-Research/Phi-3-mini-4k-instruct',
            'ChineseAlpacaGroup/llama-3-chinese-8b-instruct',
            "ZhipuAI/chatglm3-6b", revision = "v1.0.0"}
"""
# "ZhipuAI/chatglm3-6b", revision = "v1.0.0"