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
    'cookie': 'XFI=c8d375c0-b9d8-11ee-a028-2f827027eaa6; XFCS=18D13AB0AFD2248C983CC8DA91BE62A8579F00105260E79FA52CD32B9609D4F2; XFT=R4W6HzSTeKKrOT3GzvgsUTjVQuPtzCA5DevTRRvw0H0=; BAIDUID=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDUID_BFESS=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDU_WISE_UID=wapp_1687875772047_816; MCITY=-224%3A; BDUSS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; BDUSS_BFESS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; __bid_n=18d0e2f4ee62192c15e860; BIDUPSID=A56C8A24FD3AE5B0AF32AA1FB7183B58; PSTM=1705483130; H_PS_PSSID=39998_40022_40134; STOKEN=1d110694838c9ea29bb04c872e572c3ca9d32a901303f290989c3a00a400d331; arialoadData=false; ZFY=fDS4mdjJaqSBNJOqdcIpOvXYwDOTdDwlzPhb0NWLANw:C; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1705918762,1705991034,1706004992; USER_JUMP=-1; st_key_id=17; 1705483800_FRSVideoUploadTip=1; video_bubble1705483800=1; XFI=84ed9020-b9d8-11ee-a39b-b5307d5b4131; XFCS=BB4ECB4144FE0B1D44F4C1E2CDF8AC77A18903E726E6A9D4F5CEE2AEAC70CF62; XFT=qPetI9NoPGv7zh40Jr+ArhsTzg6GiHYTr4hfCt/ZeiM=; wise_device=0; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1706005092; BA_HECTOR=2g2hag0h21a025010105a020mdqovq1iqv4k31t; ab_sr=1.0.1_MTgyMzk4NTUyMTk3ZWQyMjhiNTMzZmViYTgyMmJhNjliOWVlNGRkNzExMjhkYTZiOWIwMWVhNzlkMGU4NWZmZTE1ZWU5MzcxYzdmODE5ZmRiOGZhYjRhMzhjZWVkMDc1YTIzZWNmNjAxYTk0ZWIwOWM4NWQxMTcyZDk0MGVlODcwYmMzMTFlZTNjNmU2ZDUxODgyNjJmMmRkOTkwMmUyZGNmOTFhOTZkYWQ4NTRlMmEyMjkxZTRkZjg5N2Q4ODIz; st_data=4643f61f19c8fd3d0f870afb85e37b8c771018db43fd91da9db7cce245b8645a60758451eef023e3cb95b9b7186ae4db775ceb3ec349183a9169c633133d8f164b6b80101794868f5f1e9dfe37ea71c735f9e64ea6f5a9b9dce330d6cae52b16100c20136f61ff00d998abf0b008762ddbd6b3b36e3c52c9abf6715d0c5df3e5fa7e6b1b7c3fbaa0ded67deefbf55997; st_sign=72cdfdc5; tb_as_data=d34083d384dd623c28dd6e57af860047595ec7e9f3cd92d7583e1d896f1914e4431347371fd88553003619223692f758c258e8a7a301e23b5cd6f585ad91f42cee2f06ee05d8edf6d4029698a53e862e7a8ef0ed72565792a3514728a1db9e8e7fb4c928aeb6439d94c353bccefc4981; RT="z=1&dm=baidu.com&si=fe9b85ff-3fbe-4987-b254-bba3c900ee02&ss=lrq7b3h3&sl=2&tt=3me4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3p6b"'
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
        tzid_list = [8870038277]
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
