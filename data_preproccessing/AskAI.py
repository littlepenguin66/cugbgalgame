import requests
from PIL import Image
import io
import gradio as gr
from config_manager import config
from check_proxy import check_proxy
from model_checkers import JudgeModelType
from model_handlers import HandleModel

class ModelProcessor:
    def __init__(self, config):
        self.config = config
        self.model_checkers = {
            "openai": JudgeModelType.is_openai_model,
            "zhipuai": JudgeModelType.is_zhipuai_model,
            "cogview": JudgeModelType.is_cogview_model,
            "qianwen": JudgeModelType.is_qianwen_model
        }
        self.model_handlers = {
            "openai": HandleModel.handle_openai_model,
            "zhipuai": HandleModel.handle_zhipuai_model,
            "cogview": HandleModel.handle_cogview_model,
            "qianwen": HandleModel.handle_qianwen_model
        }

    def generate_response(self, model_name, prompt, temperature):
        proxy_status = "Proxy status: Active" if self.config.USE_PROXY else "Proxy status: Inactive"
        proxy_location = "No proxy location"
        if self.config.USE_PROXY:
            try:
                proxy_location = check_proxy(self.config.proxies)
                if "无效" in proxy_location:
                    proxy_status = "Proxy status: Invalid"
            except Exception as e:
                proxy_status = "Proxy status: Invalid"
                proxy_location = str(e)
        proxy_info = f"{proxy_status}, {proxy_location}"
        for model_type, checker in self.model_checkers.items():
            if checker(model_name):
                handler = self.model_handlers[model_type]
                try:
                    if model_type == "cogview":
                        image = handler(model_name, prompt, temperature, self.config)
                        return None, None, image
                    else:
                        text = handler(model_name, prompt, temperature, self.config)
                        return text, proxy_info, None
                except Exception as e:
                    return str(e), proxy_info, None
        return "Model not found", proxy_info, None

def main():
    if config and config.USE_PROXY:
        proxies = config.proxies
        session = requests.Session()
        session.proxies.update(proxies)
    else:
        proxies = None

    processor = ModelProcessor(config)

    model_name = gr.Dropdown(choices=config.AVAIL_LLM_MODELS, label="选择模型")
    prompt = gr.Textbox(lines=8, label="输入你的问题")
    T = gr.Slider(minimum=0.1, maximum=1.0, value=config.TEMPERATURE, label="调整温度", step=0.1)

    iface = gr.Interface(
        fn=processor.generate_response,
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

if __name__ == "__main__":
    main()