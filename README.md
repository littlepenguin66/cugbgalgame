# 项目名称：综合数据处理与智能问答系统
[![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Star on Gitee](https://gitee.com/jerryzheng66/cugbgalgame/badge/star.svg?theme=dark)](https://gitee.com/jerryzheng66/cugbgalgame)
![png](https://cdn.jsdelivr.net/gh/littlepenguin66/webImage/background.png)
## 项目简介
本系统是一个结合数据处理和智能问答功能的Python应用程序。它提供了从数据获取到智能响应的一系列功能，包括：
- **数据抓取**：从百度贴吧特定板块抓取帖子内容。
- **数据处理**：进行CSV文件创建、JSON文件分割与合并、数据翻译等操作。
- **数据存储**：将处理后的数据存储至CSV和JSON文件中。
- **AI问答接口**：整合了多种AI模型，如OpenAI、ZhipuAI等，提供问答服务。
- **图像识别**：利用PaddleOCR库实现光学字符识别功能。
- **模型管理**：支持预训练AI模型的下载与管理。
- **环境配置检查**：检查PyTorch版本和CUDA配置，确保系统正常运行。
## 环境与安装
### 系统要求
- Python 3.6 或更高版本
### 依赖库
- requests
- beautifulsoup4
- pandas
- json
- gradio
- torch
- paddlepaddle
- paddleslim
- tencentcloud-sdk-python
### 安装指南
1. 克隆或下载本项目的代码。
2. 在项目根目录下执行 `pip install -r requirements.txt` 以安装所有依赖。
## 运行指导
1. 执行 `data_preproccessing/AskAI.py`，然后在浏览器中访问生成的链接，即可体验AI问答功能。
2. 运行其他Python脚本，以执行数据抓取、处理和存储等任务。
## 贡献方式
1. 在Gitee上Fork本项目。
2. 在本地创建分支，并进行代码修改。
3. 提交更改，并通过Pull Request向我们贡献你的代码。
## 许可证
本项目采用 [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).
## 示例与演示
- **AI问答**：运行 `data_preproccessing/AskAI.py`，在浏览器中输入问题，即可获得AI模型的回答。
- **图像识别**：运行 `data_preproccessing/OCR.py`，输入图片路径，程序将输出识别结果。
## 常见问题解答
1. 如何配置API密钥？
   请在 `config.py` 文件中修改相应的密钥设置。
2. 如何设置代理？
   在 `config.py` 文件中修改代理服务器设置。
## 联系我们
如有任何疑问或建议，请联系项目维护者：[little_penguin66]@[littlepenguinzq@gmail.com]。
这个项目是一个全面的数据处理和问答系统，适用于各种需要智能问答功能的场景，提供了从数据获取到智能响应的完整解决方案。
