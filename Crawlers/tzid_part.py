import requests
import re
from fake_useragent import UserAgent

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

uprange = 100000  # 爬取帖子的上限

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

def get_tzid():
    # 第二个参数是总帖子数
    # 检测tzid_list.txt以及tzid_progress文件是否存在，没有则创建
    tzid_list = []
    try:
        with open('tzid_progress.txt', 'r') as f:
            tzid = int(f.read())
    except:
        with open('tzid_progress.txt', 'w') as f:
            f.write('0')
            tzid = 0

    try:
        with open('tzid_list.txt', 'r') as f:
            pass
    except:
        with open('tzid_list.txt', 'w') as f:
            pass

    # 读取上次运行时的tzid值，以便从开始
    for i in range(tzid, uprange, 50):
        url = f'https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&ie=utf-8&pn={i}'
        response = requests.get(url, headers=headers)
        print(response)
        html = response.text
        href_list = re.findall(r'href="/p/(.*?)"', html)
        print(href_list)
        #将href_list内的帖子id加入tzid_list.txt
        with open('tzid_list.txt', 'a') as f:
            for j in href_list:
                f.write(j + '\n')
        #将i写入tzid_progress.txt
        with open('tzid_progress.txt', 'w') as f:
            f.write(str(i))
        print(i)

get_tzid()
print('ok')