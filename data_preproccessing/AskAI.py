"""
猪肉AI - 一个基于多种AI模型的Web应用

该应用提供了一个用户界面，允许用户选择不同的AI模型，输入问题，并调整生成回答的温度。应用支持多种模型类型，包括文本生成和图像生成。

主要功能：
- 支持多种AI模型，包括OpenAI、ZhipuAI、Cogview和Qianwen。
- 允许用户输入问题，并根据选择的模型生成回答。
- 提供了一个温度滑块，允许用户调整生成回答的随机性。
- 如果使用代理，会显示代理状态和位置信息。
- 对于图像生成模型，会显示生成的图片。

使用方法：
1. 运行该脚本。
2. 打开浏览器，访问显示的URL。
3. 在界面上选择一个模型。
4. 在文本框中输入你的问题。
5. 调整温度滑块（如果需要）。
6. 点击提交，查看AI的回答和代理信息。

注意：
- 该应用依赖于外部API，因此需要确保网络连接正常。
- 代理设置在配置文件中配置，如果使用代理，应用会显示代理状态和位置。
- 图像生成模型的结果会直接显示在界面上。

类和函数说明：
ModelProcessor:
   - __init__(config): 初始化模型处理器，配置模型检查器和处理函数。
   - generate_response(model_name, prompt, temperature): 根据模型名称、提示和温度生成响应。

main:
   - 设置请求会话的代理（如果使用）。
   - 创建ModelProcessor实例。
   - 定义Gradio界面，包括模型选择、提示输入和温度调整。
   - 启动Gradio界面。

依赖库：
- requests: 用于发送HTTP请求。
- PIL.Image: 用于处理图像。
- io: 用于处理流。
- gradio: 用于创建Web界面。
- config_manager: 用于管理配置。
- check_proxy: 用于检查代理状态。
- model_checkers: 用于检查模型类型。
- model_handlers: 用于处理模型生成的响应。
"""
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
        description="使用OpenAI和ZhipuAI的API生成回答,支持的模型[‘gpt-3.5-turbo’, ‘gpt-4-1106-preview’, ‘gpt-4-turbo-preview’, ‘gpt-4-vision-preview’,‘gpt-3.5-turbo-1106’, ‘gpt-3.5-turbo-16k’, ‘gpt-3.5-turbo’,'glm-4', 'glm-3','cogview-3','qwen-turbo', 'qwen-plus', 'qwen-max', 'qwen-max-0403', 'qwen-max-0107', 'qwen-max-longcontext', 'qwen-max-0428']",
    )

    iface.launch()

if __name__ == "__main__":
    main()