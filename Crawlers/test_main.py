import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from fake_useragent import UserAgent
import time

ua = UserAgent()
HEADERS = {
    'user-agent': ua.random,
    # 你的cookie信息
    'cookie': 'XFI=045e6440-b9b8-11ee-87c5-1534775ba3a8; XFCS=3200170887A4C0A5E0CFC1AAA8179612948000B715F9CBBD8C390E7E197C93DA; XFT=WWc8ZMNgD2cWPp7BvgFwZQWwNK7wLihd/sFjOWZeaqs=; BAIDUID=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDUID_BFESS=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDU_WISE_UID=wapp_1687875772047_816; MCITY=-224%3A; BDUSS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; BDUSS_BFESS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; __bid_n=18d0e2f4ee62192c15e860; BIDUPSID=A56C8A24FD3AE5B0AF32AA1FB7183B58; PSTM=1705483130; H_PS_PSSID=39998_40022_40134; STOKEN=1d110694838c9ea29bb04c872e572c3ca9d32a901303f290989c3a00a400d331; arialoadData=false; ZFY=fDS4mdjJaqSBNJOqdcIpOvXYwDOTdDwlzPhb0NWLANw:C; USER_JUMP=-1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1705918762,1705991034; st_key_id=17; 1705483800_FRSVideoUploadTip=1; video_bubble1705483800=1; XFI=fced54f0-b9b7-11ee-bfa1-c9a86b0e60d1; XFCS=5D8B76EE8645E92C6429BD3813E650178C03287C1760ECCB5A3FC3C3B6101DBD; XFT=jZZFAL2FpMK4p7UqBGqmojJhve4eONjdIUUw/jEzk28=; wise_device=0; BA_HECTOR=8la58k8l240ha4042l0l2484b7tbnr1iqums91t; ab_sr=1.0.1_ZDI5MTZkYWNiMjYyNzNhODc2MWI4YmI0MWEwNmIxYmI3MzNhOWM4ZWU0MTllNGUzNmYzYTg5NzBhNzQxYmQyZWM1NTNjOTIyMTI1ZmIyN2U3ODk1NGI0MTUwZTE3ZTZiNzM2OTk2NGFjN2JkOTAyYjUwMTg1MWEwZjkwNDVlMTVmOWU4MTNjMTAzNmI3MGM4M2NhNTkxZDVkYzcyN2VjOGM1MzY2MjYxMjJlMThkYTYzNWI3OTljZmIxMWFjM2Fh; st_data=4643f61f19c8fd3d0f870afb85e37b8c771018db43fd91da9db7cce245b8645a60758451eef023e3cb95b9b7186ae4db775ceb3ec349183a9169c633133d8f164b6b80101794868f5f1e9dfe37ea71c735f9e64ea6f5a9b9dce330d6cae52b16ef715526c1d6c615066146ba1af9d02c2584644dc28c36a211278009ecfc117aac7db80633374818b2b9baadf5627821; st_sign=927ef682; RT="z=1&dm=baidu.com&si=fe9b85ff-3fbe-4987-b254-bba3c900ee02&ss=lrpz0erb&sl=6&tt=c7q&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4bws&ul=d2hb&hd=d3ny"; tb_as_data=d34083d384dd623c28dd6e57af860047595ec7e9f3cd92d7583e1d896f1914e4431347371fd88553003619223692f7586165b9d0aaa07d2cf27f4f80a92dec0bf91a2d8ab032039dc88c6446712272c5002ed7d162be89ff7e85ca6060dc9bf683d6d4fd5b44f7230db2f70d8111d23f; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1705991653'
}

# 配置变量
COMMENT_FILE = 'tieba.csv'
POST_PROGRESS_FILE = 'tiebajindu2.txt'
THREAD_LIST_FILE = 'tzid_list.txt'
SLEEP_DURATION = 1  # 1秒的延迟以避免被网站阻塞


def get_data(tzid):
    url = f'https://tieba.baidu.com/p/{tzid}'
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"请求错误：{err}")
        return 0

    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        with open(POST_PROGRESS_FILE, 'r') as f:
            pn = int(f.read())
    except FileNotFoundError:
        with open(POST_PROGRESS_FILE, 'w') as f:
            f.write('1')
        pn = 1

    page = soup.find_all('li', class_='l_reply_num')
    page = page[0].text
    page = re.findall(r'\d+', page)
    page = int(page[1])

    for pg in range(pn, page):
        with open(POST_PROGRESS_FILE, 'w') as f:
            f.write(str(pg))
        url = f'https://tieba.baidu.com/p/{tzid}?pn={pg}'
        if not get_content(url):
            return 0


def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"请求错误：{err}")
        return 0

    if r.status_code == 200:
        comment_list = []
        soup = BeautifulSoup(r.text, 'lxml')
        comment_list.extend(extract_comments(soup, 'div', 'd_post_content j_d_post_content'))
        comment_list.extend(extract_comments(soup, 'div', 'lzl_content_main'))

        if not comment_list:
            return 0

        df = pd.DataFrame(comment_list, columns=['评论'])
        df.to_csv(COMMENT_FILE, mode='a', index=False, header=False)
    else:
        print('结束')
    return 0


def extract_comments(soup, tag, class_name):
    comment_list = []
    comments = soup.find_all(tag, class_=class_name)
    for comment in comments:
        text = re.sub('<.*?>', '', str(comment))
        if len(text) >= 31:
            comment_list.append(text)
    return comment_list


def get_thread_ids():
    try:
        with open(THREAD_LIST_FILE, 'r') as f:
            tzid_list = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        tzid_list = []
        print('重新记录帖子id')
        for pa in range(0, 800, 50):
            url = f'https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&ie=utf-8&pn={pa}'
            try:
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"请求错误：{err}")
                return 0

            html = response.text
            href_list = re.findall(r'href="/p/(.*?)"', html)
            tzid_list.extend(href_list)
        with open(THREAD_LIST_FILE, 'w') as f:
            for tzid in tzid_list:
                f.write(tzid + '\n')

    try:
        with open(POST_PROGRESS_FILE, 'r') as f:
            n = int(f.read())
    except FileNotFoundError:
        with open(POST_PROGRESS_FILE, 'w') as f:
            f.write('1')
        n = 1

    for tzs in range(n, len(tzid_list)):
        with open(POST_PROGRESS_FILE, 'w') as f:
            f.write(str(n))
        if not get_data(tzid_list[tzs]):
            print('内容为空，中断')
            return 0
        n += 1
        time.sleep(SLEEP_DURATION)


# 检测是否有 COMMENT_FILE 文件，如果没有则创建
try:
    pd.read_csv(COMMENT_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=['评论'])
    df.to_csv(COMMENT_FILE, index=False, encoding='utf_8_sig')

get_thread_ids()
print('ok')
