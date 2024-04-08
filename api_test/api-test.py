# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))

#读取中文文本
with open ("text.txt", "r", encoding="utf-8") as f:
    text = f.read()

MODEL = "gpt-3.5-turbo"
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "assistant", "content": "你好，我是一个自动文本生成机器人，我可以帮助你将文本转化为指定格式。"},
        {"role": "user", "content": "务必记住content是文章所描述的具体对象，summary是对该对象的描述，若有多个具体对象则相应生成多对content与summary，每一组均有一对{}"},
        {"role": "user", "content": "content的内容应尽可能精确，避免出现多个对象的描述，summary的内容应尽可能简洁，避免过于冗长。"},
        {"role": "user", "content": '请你将以下这段文字转化为若干{"content": "","summary": ""}的格式，content内容为文章描述的具体对象，summary为对该对象的描述,若有多个具体对象则相应生成多对content与summary，每一组均有一对{}' + text},
    ],
    temperature=0,
)
#仅输出content部分
print(response.choices[0].message.content)
