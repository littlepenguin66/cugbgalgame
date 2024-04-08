import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from fake_useragent import UserAgent
from time import sleep
import json
import datetime
import os


#尝试读取cookies.
try:
    with open('cookies.txt', 'r') as f:
        #读取文件中cookies，每个cookies用";"隔开
        cookies = f.read()
#失败则创建cookies.txt文件并中断程序
except:
    with open('cookies.txt', 'w') as f:
        f.write('cookies')
    print('请在cookies.txt文件中输入cookies')
    exit()
#打开网页并获取cookies
def get_cookies(url):



uprange = 1000  # 爬取帖子的上限
downrange = 1 # 爬取帖子的下限

# 获取当前时间并转换为字符串格式
current_time = datetime.datetime.now().strftime('%Y%m%d%H')

ua = UserAgent()
comment_list_check = []
headers = {
    'Host': 'tieba.baidu.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': cookies
}


def get_data(tzid):
    url1 = f'https://tieba.baidu.com/p/{tzid}'

    # 检测是否有tiebajindu2.txt文件，如果没有则创建
    try:
        with open('tiebajindu2.txt', 'r') as f:
            pass
    except:
        with open('tiebajindu2.txt', 'w') as f:
            f.write('2')
    # 读取上次运行时的pn值，以便从pn开始
    with open('tiebajindu2.txt', 'r') as f:
        pn = int(f.read())

    print(url1)

    for pg in range(pn, 1145):
        # 保存pn的值
        with open('tiebajindu2.txt', 'w') as f:
            f.write(str(pg))
        url = f'https://tieba.baidu.com/p/totalComment?tid={tzid}=&pn={pg}&see_lz=0'
        r1 = get_content(url)
        if r1 == 0:
            return 0
        elif r1 == 1:
            print('该帖子已结束')
            break
    # tiebajindu2.txt文件中的pn值到达最大值时，将pn值重置为2
    with open('tiebajindu2.txt', 'w') as f:
        f.write('2')


def get_content(url):
    r = requests.get(url, headers=headers)
    global comment_list_check
    # 导入为json格式
    js = json.loads(r.text)
    if r.status_code == 200:
        if 'comment_list' not in js['data']:
            return 1
        elif js['data']['comment_list'] == []:
            return 1
        else:
            comment_list1 = []
            comment_list = js["data"]["comment_list"]
            for comment_id, comment_info in comment_list.items():
                for comment in comment_info["comment_info"]:
                    content = comment["content"]
                    content = re.sub('<.*?>', '', content)
                    print("评论:", content)
                    if len(content) >= 31:
                        comment_list1.append(content)
        output_dir = '../Crawlers/Data/csv' # 保存路径
        file_name_path = '../Crawlers/Data/file_name.txt' # 保存文件名
        if comment_list1 == comment_list_check: # 检测是否有新的评论
            return 1
        df = pd.DataFrame(comment_list1, columns=['评论']) # 创建DataFrame
        filename = current_time + 'tieba.csv' # 创建文件名
        df.to_csv(os.path.join(output_dir, filename), mode='a', index=False, header=False) # 保存文件
        if not os.path.exists(os.path.join(output_dir, filename)):
            with open(file_name_path, 'a') as file:
                file.write(filename + '\n')
        comment_list_check = comment_list1 # 更新评论列表
    else:
        print('over')
        return 0


def get_tzid():
    # 第二个参数是总帖子数
    # 检测tzid_list.txt文件是否存在，如果存在则读取，如果不存在则创建
    try:
        tzid_list = []
        with open('tzid_list.txt', 'r') as f:
            for line in f.readlines():
                tzid_list.append(line.strip())

    except:
        # 创建一个空的列表
        tzid_list = []
        for i in range(downrange, uprange, 50):
            url = f'https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&ie=utf-8&pn={i}'
            response = requests.get(url, headers=headers)
            html = response.text
            href_list = re.findall(r'href="/p/(.*?)"', html)
            tzid_list.extend(href_list)
        print('重新记录帖子id')
        # 保存帖子id
        with open('tzid_list.txt', 'w') as f://
            for tzid in tzid_list:
                f.write(tzid + '\n')
    # 检测是否有tiebajindu.txt文件，如果没有则创建
    try:
        with open('tiebajindu.txt', 'r') as f:
            pass
    except:
        with open('tiebajindu.txt', 'w') as f:
            f.write('2')
    # 读取上次运行时的n值，以便从n开始
    with open('tiebajindu.txt', 'r') as f:
        n = int(f.read())
    for i in range(n, len(tzid_list)):
        # 储存n的值，以便下次运行时从n开始
        with open('tiebajindu.txt', 'w') as f:
            f.write(str(n))
        if get_data(tzid_list[i]) == 0:
            print('内容为空，中断')
            return 0
            break
        n += 1

get_tzid()
print('ok')