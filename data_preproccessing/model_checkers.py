class JudgeModelType:
    """
        判断模型类型的工具类。

        这个类提供了一系列静态方法，用于判断给定的模型名称是否属于特定的模型类型。
        每个方法都接受一个模型名称作为参数，并返回一个布尔值，指示该模型名称是否与特定类型匹配。

        Methods:
            is_openai_model(model_name): 判断模型名称是否为OpenAI模型。
            is_zhipuai_model(model_name): 判断模型名称是否为智谱AI模型。
            is_cogview_model(model_name): 判断模型名称是否为Cogview模型。
            is_qianwen_model(model_name): 判断模型名称是否为Qianwen模型。
    """
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