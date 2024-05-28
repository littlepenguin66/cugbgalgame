"""
    尝试导入配置模块并返回配置对象。

    这个函数首先尝试导入名为 `config_private` 的模块，如果失败，则尝试导入名为 `config` 的模块。
    如果两个模块都找不到，函数将打印一条错误消息，并返回 `None`。

    Returns:
        module or None: 如果成功导入配置模块，则返回该模块对象；如果都失败，则返回 `None`。
"""
try:
    import config_private as config
except ImportError:
    try:
        import config as config
    except ImportError:
        print("No configuration file found.")
        config = None
