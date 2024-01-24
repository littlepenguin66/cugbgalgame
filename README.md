# 大语言模型游戏应用项目
本项目是开发和训练的大语言模型项目，专注于为游戏行业提供高级语言处理功能。
## 项目结构
### 爬虫部分
- `Crawlers/`: 存放爬虫相关代码和配置文件。
  - `tieba_spider.py`: 百度贴吧帖子内容和评论的爬虫脚本。
  - `THREAD_LIST_FILE`: 存储要抓取的帖子ID列表的文件。
  - `HEADERS`: 存储请求头信息的配置文件。
  - `COMMENT_FILE`: 存储抓取到的评论数据的CSV文件。
  - `POST_PROGRESS_FILE`: 存储爬虫进度信息的文件。
- #### 爬虫概述
  - 爬虫部分主要针对百度贴吧，通过配置特定的贴吧关键词和帖子ID，抓取相关的帖子内容和评论。这些数据将用于训练和优化大语言模型，以更好地服务于游戏行业的应用需求。
- #### 安装指南
  - 在运行爬虫之前，请确保您的环境中已安装以下依赖库：
  - `requests`
  - `BeautifulSoup`
  - `pandas`
  - `fake_useragent`
- 您可以使用以下命令进行安装：
```bash
pip install -r requirements.txt
```
- #### 使用说明
  - 1.在 `THREAD_LIST_FILE` 中设置您要抓取的帖子ID列表。
  - 2.在 `HEADERS` 中配置您的 `cookie` 信息。
  - 3.运行 `test.main.py` 脚本，程序将自动抓取并保存帖子内容和评论。
- #### 功能特性
- 抓取特定贴吧的帖子内容和评论。
- 支持分页抓取。
- 将抓取到的数据保存为 CSV 文件。
### 大语言模型部分
- 正在开发
## 贡献指南
如果您想为此项目贡献代码，请遵循以下步骤：
1. Fork 本项目。
2. 创建您的特性分支 (`git checkout -b my-new-feature`)。
3. 提交您的改动 (`git commit -am 'Add some feature'`)。
4. 将您的改动推送到分支 (`git push origin my-new-feature`)。
5. 打开一个 Pull Request。
## 许可证信息
本项目使用 AGPL-3.0 许可证。
## 联系信息
或有任何建议，欢迎通过以下方式联系：
- 刷视频去：[哈哈哈](www.bilibili.com)
---
