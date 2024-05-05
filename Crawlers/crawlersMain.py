import requests
import re
from bs4 import BeautifulSoup  # 引入BS库
import fake_useragent

ua = fake_useragent.UserAgent()

# 实现run方法
# 1.url列表
# 2.遍历,发送请求,获取响应
# 3.保存

class TiebaSpider:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.url_temp = "https://tieba.baidu.com/f?kw=" + tieba_name + "&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": ua.random
        }

    def get_url_list(self):  # 构造url列表
        # url_list = []
        # for i in range(1000):
        #     url_list.append(self.url_temp.format(i * 50))
        # return url_list
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
                # 因为转为json后\n不胡自动换行，所以我们这里将\n给手换行
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
        # print(new_html)
        soup = BeautifulSoup(new_html, 'lxml')
        all_result = soup.find_all(class_='threadlist_abs_onlyline')
        list = []
        for i in all_result:
            # new_i = clean_space(i.get_text())
            new_i = re.sub('\s+', '', i.get_text()).strip()
            if new_i != '':  # print('此选项为空!!!')
                list.append(new_i)
                print(new_i)
        self.write(list, self.tieba_name)

        # print(list)
        # print(all_result)
        # file_path = "{}-第{}页.html".format(self.tieba_name, page_num)
        # with open(file_path, "w", encoding="utf-8") as f:  # 李毅-第1页.html
        #     f.write(html_str)

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_url(url)
            # 保存
            page_num = url_list.index(url) + 1
            self.save_html(html_str, page_num)


if __name__ == '__main__':
    tieba_spider = TiebaSpider("孙笑川")
    tieba_spider.run()

