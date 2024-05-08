# 模型下载
from modelscope import snapshot_download

model_dir = snapshot_download('LLM-Research/Phi-3-mini-4k-instruct', cache_dir='~/models')

model_id = {'baicai003/Phi-3-mini-128k-instruct-Chinese',
            'LLM-Research/Phi-3-mini-4k-instruct',
            'ZhipuAI/chatglm3-6b'}
# "ZhipuAI/chatglm3-6b", revision = "v1.0.0"
