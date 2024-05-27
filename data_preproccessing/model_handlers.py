
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