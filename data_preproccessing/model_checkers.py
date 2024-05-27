class JudgeModelType:
    @staticmethod
    def is_openai_model(model_name):
        openai_models = ["gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-4-turbo-preview", "gpt-4-vision-preview",
                         "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
        return model_name in openai_models

    @staticmethod
    def is_zhipuai_model(model_name):
        zhipuai_models = ["glm-4", "glm-3"]
        return model_name in zhipuai_models

    @staticmethod
    def is_cogview_model(model_name):
        cogview_models = ["cogview-3"]
        return model_name in cogview_models

    @staticmethod
    def is_qianwen_model(model_name):
        qianwen_models = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-0403", "qwen-max-0107", "qwen-max-longcontext", "qwen-max-0428"]
        return model_name in qianwen_models