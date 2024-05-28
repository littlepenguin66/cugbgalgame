"""
百度贴吧爬虫 - 用于抓取百度贴吧帖子列表

使用方法：
1. 确保已安装所有必需的库，包括requests, BeautifulSoup, fake_useragent。
2. 运行程序，输入您想要抓取的贴吧名称。
3. 程序将自动抓取前50页的帖子列表，并将帖子标题保存到文本文件中。

类和方法说明：
TiebaSpider类:
__init__(tieba_name): 初始化贴吧爬虫，需要提供贴吧名称。
get_url_list(): 构造贴吧帖子的URL列表。
parse_url(url): 发送请求并获取网页内容。
del_title(no_html): 清除HTML中的注释。
write(content, txt_name): 将内容写入文本文件。
save_html(html_str, page_num): 解析HTML并保存帖子标题。
run(): 执行爬虫的主循环。

注意：
- 请确保遵守目标网站的使用协议和爬虫策略。
- 网络请求可能受到目标网站的反爬虫措施影响，请合理使用。
- 程序仅供学习和研究使用，请勿用于商业或非法用途。
"""
import sys
import requests
import re
from bs4 import BeautifulSoup
import fake_useragent

ua = fake_useragent.UserAgent()

class TiebaSpider:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.url_temp = "https://tieba.baidu.com/f?kw=" + tieba_name + "&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": ua.random
        }

    def get_url_list(self):  # 构造url列表
        return [self.url_temp.format(i * 50) for i in range(50)]

    def parse_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def del_title(self, no_html):
        # 删除 <!--或者 -->
        new_html = re.sub(r'<!--|-->', '', no_html, 2)
        return new_html

    def write(self, content, txt_name):
        # 打开一个文件,将列表的内容一行一行的存储下来
        with open(txt_name + '.txt', 'a', encoding='UTF-8') as f:
            for i in range(len(content)):
                # 因为转为json后\n不会自动换行，所以我们这里将\n手动换行
                string = content[i].split("\\n")
                for i in string:
                    # 打印每条评论
                    print(i)
                    # 将评论写入文本
                    f.writelines(i)
                    # 给评论换行
                    f.write("\n")

    def save_html(self, html_str, page_num):
        print(html_str)
        match = re.findall('(?s)<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list".*?</code>',
                           html_str)
        html = match[0]
        new_html = self.del_title(html)
        soup = BeautifulSoup(new_html, 'lxml')
        all_result = soup.find_all(class_='threadlist_abs_onlyline')
        list = []
        for i in all_result:
            new_i = re.sub('\s+', '', i.get_text()).strip()
            if new_i != '':
                list.append(new_i)
                print(new_i)
        self.write(list, self.tieba_name)

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_url(url)
            # 保存
            page_num = url_list.index(url) + 1
            self.save_html(html_str, page_num)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python crawlersMain.py <tieba_name>")
    else:
        tieba_name = sys.argv[1]
        tieba_spider = TiebaSpider(tieba_name)
        tieba_spider.run()


