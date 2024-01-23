import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'user-agent': ua.random,
    'cookie': 'XFI=045e6440-b9b8-11ee-87c5-1534775ba3a8; XFCS=3200170887A4C0A5E0CFC1AAA8179612948000B715F9CBBD8C390E7E197C93DA; XFT=WWc8ZMNgD2cWPp7BvgFwZQWwNK7wLihd/sFjOWZeaqs=; BAIDUID=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDUID_BFESS=A56C8A24FD3AE5B0AF32AA1FB7183B58:FG=1; BAIDU_WISE_UID=wapp_1687875772047_816; MCITY=-224%3A; BDUSS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; BDUSS_BFESS=mFwa21mMENNfkpZZ3QyR1hTNTF-RmZuTi1BZHEzTlZVQ0lTTndoaTB0VjJ1YlZsRVFBQUFBJCQAAAAAAAAAAAEAAAAYnqdl09qzx3oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYsjmV2LI5le; __bid_n=18d0e2f4ee62192c15e860; BIDUPSID=A56C8A24FD3AE5B0AF32AA1FB7183B58; PSTM=1705483130; H_PS_PSSID=39998_40022_40134; STOKEN=1d110694838c9ea29bb04c872e572c3ca9d32a901303f290989c3a00a400d331; arialoadData=false; ZFY=fDS4mdjJaqSBNJOqdcIpOvXYwDOTdDwlzPhb0NWLANw:C; USER_JUMP=-1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1705918762,1705991034; st_key_id=17; 1705483800_FRSVideoUploadTip=1; video_bubble1705483800=1; XFI=fced54f0-b9b7-11ee-bfa1-c9a86b0e60d1; XFCS=5D8B76EE8645E92C6429BD3813E650178C03287C1760ECCB5A3FC3C3B6101DBD; XFT=jZZFAL2FpMK4p7UqBGqmojJhve4eONjdIUUw/jEzk28=; wise_device=0; BA_HECTOR=8la58k8l240ha4042l0l2484b7tbnr1iqums91t; ab_sr=1.0.1_ZDI5MTZkYWNiMjYyNzNhODc2MWI4YmI0MWEwNmIxYmI3MzNhOWM4ZWU0MTllNGUzNmYzYTg5NzBhNzQxYmQyZWM1NTNjOTIyMTI1ZmIyN2U3ODk1NGI0MTUwZTE3ZTZiNzM2OTk2NGFjN2JkOTAyYjUwMTg1MWEwZjkwNDVlMTVmOWU4MTNjMTAzNmI3MGM4M2NhNTkxZDVkYzcyN2VjOGM1MzY2MjYxMjJlMThkYTYzNWI3OTljZmIxMWFjM2Fh; st_data=4643f61f19c8fd3d0f870afb85e37b8c771018db43fd91da9db7cce245b8645a60758451eef023e3cb95b9b7186ae4db775ceb3ec349183a9169c633133d8f164b6b80101794868f5f1e9dfe37ea71c735f9e64ea6f5a9b9dce330d6cae52b16ef715526c1d6c615066146ba1af9d02c2584644dc28c36a211278009ecfc117aac7db80633374818b2b9baadf5627821; st_sign=927ef682; RT="z=1&dm=baidu.com&si=fe9b85ff-3fbe-4987-b254-bba3c900ee02&ss=lrpz0erb&sl=6&tt=c7q&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4bws&ul=d2hb&hd=d3ny"; tb_as_data=d34083d384dd623c28dd6e57af860047595ec7e9f3cd92d7583e1d896f1914e4431347371fd88553003619223692f7586165b9d0aaa07d2cf27f4f80a92dec0bf91a2d8ab032039dc88c6446712272c5002ed7d162be89ff7e85ca6060dc9bf683d6d4fd5b44f7230db2f70d8111d23f; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1705991653'
    }
def get_data(tzid):
    url1 = f'https://tieba.baidu.com/p/{tzid}'
    res = requests.get(url1, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    #检测是否有tiebajindu2.txt文件，如果没有则创建
    try:
        with open('tiebajindu2.txt', 'r') as f:
            pass
    except:
        with open('tiebajindu2.txt', 'w') as f:
            f.write('1')
    #读取上次运行时的pn值，以便从pn开始
    with open('tiebajindu2.txt', 'r') as f:
        pn = int(f.read())
    page = soup.find_all('li', class_='l_reply_num')
    page = page[0].text
    page = re.findall(r'\d+', page)
    page = int(page[1])
    for pg in range(pn, page):
        #保存pn的值
        with open('tiebajindu2.txt', 'w') as f:
            f.write(str(pg))
        url = f'https://tieba.baidu.com/p/{tzid}?pn={pg}'
        get_content(url)
        if get_content(url) == 0:
            return 0

def get_content(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        comment_list3 = []
        soup = BeautifulSoup(r.text, 'lxml')
        comment_list1 = soup.find_all('div', class_='d_post_content j_d_post_content')
        for i in range(len(comment_list1)):
            comment_list1[i] = re.sub('<.*?>', '', str(comment_list1[i]))
            #删去评论总长度小于2的评论
            print(len(comment_list1[i]))
            if len(comment_list1[i]) < 31:
                pass
            else:
                comment_list3.append(comment_list1[i])
        comment_list2 = soup.find_all('div', class_='lzl_content_main')
        for i in range(len(comment_list2)):
            comment_list2[i] = re.sub('<.*?>', '', str(comment_list2[i]))
            if len(comment_list2[i]) < 31:
                pass
            else:
                comment_list3.append(comment_list2[i])
        #如果没有评论则返回0
        if comment_list3 == []:
            return 0
        df = pd.DataFrame(comment_list3)
        #添加至tieba.csv文件中
        df.to_csv('tieba.csv', mode='a', index=False, header=False)
    else:
        print('over')
        return 0

def get_tzid():
    #第二个参数是总帖子数
    #检测tzid_list.txt文件是否存在，如果存在则读取，如果不存在则创建
    try:
        tzid_list = []
        with open('tzid_list.txt', 'r') as f:
            for line in f.readlines():
                tzid_list.append(line.strip())
        print('重新记录帖子id')
    except:
        tzid_list = []
        for pa in range(0, 800, 50):
            url = f'https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&ie=utf-8&pn={pa}'
            response = requests.get(url, headers=headers)
            html = response.text
            href_list = re.findall(r'href="/p/(.*?)"', html)
            tzid_list.extend(href_list)
    #保存帖子id
        with open('tzid_list.txt', 'w') as f:
            for tzid in tzid_list:
                f.write(tzid + '\n')
    #检测是否有tiebajindu.txt文件，如果没有则创建
    try:
        with open('tiebajindu.txt', 'r') as f:
            pass
    except:
        with open('tiebajindu.txt', 'w') as f:
            f.write('1')
    #读取上次运行时的n值，以便从n开始
    with open('tiebajindu.txt', 'r') as f:
        n = int(f.read())
    for tzs in range(n,len(tzid_list)):
        #储存n的值，以便下次运行时从n开始
        with open('tiebajindu.txt', 'w') as f:
            f.write(str(n))
        get_data(tzid_list[tzs])
        if get_data(tzid_list[tzs]) == 0:
            print('内容为空，中断')
            return 0
            break
        n += 1

#检测是否有tieba.csv文件，如果没有则创建
try:
    pd.read_csv('tieba.csv')
except:
    df = pd.DataFrame(columns=['评论'])
    df.to_csv('tieba.csv', index=False, encoding='utf_8_sig')
get_tzid()
print('ok')


