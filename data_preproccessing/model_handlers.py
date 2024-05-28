"""
HandleModel - 用于处理不同AI模型的请求

这个类包含了静态方法，用于处理不同类型的AI模型请求，包括文本生成和图像生成。

类方法说明：
handle_openai_model(model_name, prompt, temperature, config):
 - 处理OpenAI模型的请求。
 - 使用OpenAI API的客户端来生成文本响应。
 - 返回生成的文本内容。

handle_zhipuai_model(model_name, prompt, temperature, config):
 - 处理ZhipuAI模型的请求。
 - 使用ZhipuAI API的客户端来生成文本响应。
 - 返回生成的文本内容。

handle_cogview_model(model_name, prompt, temperature, config):
 - 处理图像生成模型的请求。
 - 使用ZhipuAI API的客户端来生成图像。
 - 请求图像的URL，下载图像数据，并返回一个PIL图像对象。

handle_qianwen_model(model_name, prompt, temperature, config):
 - 处理Qianwen模型的请求。
 - 使用OpenAI API的客户端来生成文本响应，但指定了不同的基础URL。
 - 返回生成的文本内容，或者在发生异常时返回错误信息。

使用方法：
1. 导入HandleModel类。
2. 调用相应的处理方法，传入模型名称、提示、温度和配置。
3. 方法将返回生成的响应或图像。

注意：
- 这些方法都是静态的，可以直接通过类名调用。
- 每个方法都需要相应的API密钥，这些密钥应该包含在配置对象中。
- 图像生成方法会下载图像数据，并返回一个PIL图像对象。
- 错误处理包括捕获异常并返回错误信息。
"""
class HandleModel:
    @staticmethod
    def handle_openai_model(model_name, prompt, temperature, config):
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content

    @staticmethod
    def handle_zhipuai_model(model_name, prompt, temperature, config):
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=config.ZHIPUAI_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content

    @staticmethod
    def handle_cogview_model(model_name, prompt, temperature, config):
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=config.ZHIPUAI_API_KEY)
        response = client.images.generations(
            model=model_name,
            prompt=prompt,
        )
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_data))
        return image

    @staticmethod
    def handle_qianwen_model(model_name, prompt, temperature, config):
        from openai import OpenAI
        client = OpenAI(
            api_key=config.QIANWEN_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            return 'Error message: %s' % str(e)