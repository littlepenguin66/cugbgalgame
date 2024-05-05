# CUGBGALGAME 项目文档
## 项目概述
本项目包含了一系列的Python脚本，用于数据抓取、处理和与AI模型交互。每个脚本都有其特定功能，包括配置设置、爬虫操作、数据预处理和AI模型交互等。
## 脚本列表及功能描述
| 文件路径                        | 功能描述 Lichtly                        |
|---------------------------------|---------------------------------------|
| `\config.py`    | 设置项目配置，包括代理、API密钥和模型配置。    |
| `\Crawlers\crawlersMain.py` | 主爬虫程序，用于抓取百度贴吧的帖子内容。 |
| `\dataset_procession\create_csv.py` | 创建一个空的CSV文件，用于存储文本内容和摘要。 |
| `\dataset_procession\read_csv.py` | 读取CSV文件，处理数据，并将其转换为JSON格式。 |
| `\data_preproccessing\AskAI.py` | 与AI模型交互，处理不同模型的请求。 |
| `\data_preproccessing\check_proxy.py` | 检查代理服务器配置是否有效。 |
| `\data_preproccessing\OCR.py` | 使用PaddleOCR进行图像文字识别。 |
| `\data_preproccessing\separateWord.py` | 对中文文本进行分词处理。 |

## 使用说明
1. 确保已安装所有必要的Python库。
2. 根据需要修改`config.py`中的配置项，可以新建`config_private.py`，其优先级大于`config.py`。
3. 运行相应的脚本以执行所需的功能。
## 注意事项
- 确保所有文件路径正确无误。
- 在使用API密钥时，请注意保密，避免泄露。
- 根据需要调整脚本中的参数。
