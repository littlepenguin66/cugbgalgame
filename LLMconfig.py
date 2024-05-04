# 请不要直接运行此文件，运行useAPI.py

USE_PROXY = True
if USE_PROXY:
    """
    代理网络的地址，打开你的代理软件查看代理协议(socks5h / http)、地址(localhost)和端口(11284)
    填写格式是 [协议]://  [地址] :[端口]，填写之前不要忘记把USE_PROXY改成True，如果直接在海外服务器部署，此处不修改
            <配置教程&视频教程> https://github.com/binary-husky/gpt_academic/issues/1>
    [协议] 常见协议无非socks5h/http; 例如 v2**y 和 ss* 的默认本地协议是socks5h; 而cl**h 的默认本地协议是http
    [地址] 填localhost或者127.0.0.1（localhost意思是代理软件安装在本机上）
    [端口] 在代理软件的设置里找。虽然不同的代理软件界面不一样，但端口号都应该在最显眼的位置上
    """
    proxies = {
        #          [协议]://  [地址]  :[端口]
        "http": "socks5h://localhost:11284",  # 再例如  "http":  "http://127.0.0.1:7890",
        "https": "socks5h://localhost:11284",  # 再例如  "https": "http://127.0.0.1:7890",
    }
else:
    proxies = None

OPENAI_API_KEY = "your api key here"

ZHIPUAI_API_KEY = "a955965374911f40f2a1c16fbaf13872.FoGwVupI7yXnQLJC"

LLM_MODEL = "glm-4"  # 可选 ↓↓↓
AVAIL_LLM_MODELS = ["gpt-3.5-turbo", "glm-4", "glm-3", "cogview-3", "gpt-4-1106-preview", "gpt-4-turbo-preview",
                    "gpt-4-vision-preview", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]

# 选择温度
TEMPERATURE = 0.8

Message = {"role": "user", "content": ""}

if __name__ == "__main__":
    print("请不要直接运行此文件，运行useAPI.py")
    print("Please do not run this file directly, run data_proccessing.py")
    exit(0)
