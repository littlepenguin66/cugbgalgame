# Large Language Model Game Application Project
This project involves the development and training of a large language model that is specifically focused on providing advanced language processing capabilities for the gaming industry.
## Project Structure
### Crawler Section
- `Crawlers/`: Houses the code and configuration files related to web crawling.
  - `tieba_spider.py`: A script for crawling post content and comments from Baidu Tieba.
  - `THREAD_LIST_FILE`: A file that stores a list of thread IDs to be crawled.
  - `HEADERS`: A configuration file storing header information for requests.
  - `COMMENT_FILE`: A CSV file to store the crawled comment data.
  - `POST_PROGRESS_FILE`: A file to store the progress information of the crawler.
- #### Crawler Overview
  - The crawler is primarily targeted at Baidu Tieba, capturing relevant post content and comments by configuring specific Tieba keywords and thread IDs. This data is used to train and optimize the large language model, better serving the application needs of the gaming industry.
- #### Installation Guide
  - Before running the crawler, ensure that the following dependency libraries are installed in your environment:
  - `requests`
  - `BeautifulSoup`
  - `pandas`
  - `fake_useragent`
- You can install them using the following command:
```bash
pip install requests beautifulsoup4 pandas fake-useragent
```
- #### Usage Instructions
  - 1. Set the thread IDs you wish to crawl in the `THREAD_LIST_FILE`.
  - 2. Configure your `cookie` information in the `HEADERS`.
  - 3. Run the `test.main.py` script, and the program will automatically crawl and save post content and comments.
- #### Features
- Crawls post content and comments from specific Tieba forums.
- Supports paginated crawling.
- Saves the crawled data as a CSV file.
### Large Language Model Section
- Under Development
## Contribution Guidelines
If you would like to contribute code to this project, please follow these steps:
1. Fork this project.
2. Create a feature branch (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push your changes to the branch (`git push origin my-new-feature`).
5. Open a Pull Request.
## License Information
This project is licensed under the MIT License.
## Contact Information
If you encounter any issues while using this project or have any suggestions, please feel free to contact me via the following:
- Bilibili: [ahaha](www.bilibili.com)
