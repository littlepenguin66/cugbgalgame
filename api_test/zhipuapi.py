from zhipuai import ZhipuAI

client = ZhipuAI(api_key="83edf8e74ea585562cc46886023c6086.FRnRwwCmiF05NyO2") # 填写您自己的APIKey

#读取中文文本
with open ("text.txt", "r", encoding="utf-8") as f:
    text = f.read()

response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "assistant", "content": "你好，我是一个自动文本生成机器人，我可以帮助你将文本转化为指定格式。"},
        {"role": "user","content": "务必记住content是文章所描述的具体对象，summary是对该对象的描述，若有多个具体对象则相应生成多对content与summary，每一组均有一对{}"},
        {"role": "user","content": "content的内容应尽可能精确，避免出现多个对象的描述，summary的内容应尽可能简洁，避免过于冗长。"},
        {"role": "user","content": '请你将以下这段文字转化为若干{"content": "","summary": ""}的格式，content内容为文章描述的具体对象，summary为对该对象的描述,若有多个具体对象则相应生成多对content与summary，每一组均有一对{}' + text},
    ],
)
print(response.choices[0].message.content)