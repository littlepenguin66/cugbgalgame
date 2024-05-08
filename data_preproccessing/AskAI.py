try:
    import config_private as config
except:
    import config as config
from check_proxy import check_proxy
import gradio as gr
import requests
from PIL import Image
import io


def is_openai_model(model_name):
    openai_models = ["gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-4-turbo-preview", "gpt-4-vision-preview",
                     "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
    return model_name in openai_models


def is_zhipuai_model(model_name):
    zhipuai_models = ["glm-4", "glm-3"]
    return model_name in zhipuai_models


def is_cogview_model(model_name):
    cogview_models = ["cogview-3"]
    return model_name in cogview_models


def handle_openai_model(model_name, prompt, Tempereture):
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=Tempereture,
    )
    return response.choices[0].message.content


def handle_zhipuai_model(model_name, prompt, Tempereture):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=config.ZHIPUAI_API_KEY)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=Tempereture,
    )
    return response.choices[0].message.content


def handle_cogview_model(model_name, prompt, Tempereture):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=config.ZHIPUAI_API_KEY)
    response = client.images.generations(
        model=model_name,  # 填写需要调用的模型名称
        prompt=prompt,
    )
    image_url = response.data[0].url
    image_data = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_data))
    return image


def generate_response(model_name, prompt, Tempereture):
    proxy_status = "Proxy status: Active" if config.USE_PROXY else "Proxy status: Inactive"
    proxy_location = "No proxy location"
    if config.USE_PROXY:
        try:
            proxy_location = check_proxy(config.proxies)
            if "无效" in proxy_location:
                proxy_status = "Proxy status: Invalid"
        except Exception as e:
            proxy_status = "Proxy status: Invalid"
            proxy_location = str(e)
    proxy_info = f"{proxy_status}, {proxy_location}"
    model_handlers = {
        "openai": handle_openai_model,
        "zhipuai": handle_zhipuai_model,
        "cogview": handle_cogview_model
    }
    for model_type, handler in model_handlers.items():
        if globals()[f"is_{model_type}_model"](model_name):
            try:
                if model_type == "cogview":
                    image = handler(model_name, prompt, Tempereture)
                    return None, None, image
                else:
                    text = handler(model_name, prompt, Tempereture)
                    return text, proxy_info, None
            except Exception as e:
                return str(e), proxy_info, None
    return "Model not found", proxy_info, None


if __name__ == "__main__":
    if config.USE_PROXY:
        proxies = config.proxies
        requests.default_proxies = proxies
    else:
        proxies = None
    model_name = gr.Dropdown(choices=config.AVAIL_LLM_MODELS, label="选择模型")
    prompt = gr.Textbox(lines=8, label="输入你的问题")
    T = gr.Slider(minimum=0.1, maximum=1.0, value=config.TEMPERATURE, label="调整温度", step=0.1)

    iface = gr.Interface(
        fn=generate_response,
        inputs=[model_name, prompt, T],
        outputs=[
            gr.TextArea(label="AI回答"),
            gr.Textbox(label="代理信息"),
            gr.Image(label="AI生成的图片"),
        ],
        title="欢迎使用猪肉AI",
        description="使用OpenAI和ZhipuAI的API生成回答",
    )

    iface.launch()
