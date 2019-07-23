import json
import random
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import tqdm
import os
import csv
import hashlib
from requests.cookies import RequestsCookieJar
from urllib import error
from pymongo import MongoClient

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Host': 'api.bilibili.com',
    # 'Upgrade-Insecure-Requests': '1',
    # 'If-None-Match': hashlib.md5(str(int(time.time())).encode('utf-8')).hexdigest(),
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    'User-Agent': random.choice(UA_LIST)
}




def get_av_list(index):
    """
    根据页码获取视频av号
    :param index:
    :return:
    """
    # duration=1 表示取时长在10分钟以下的
    root_url = 'https://search.bilibili.com/all?keyword=食品安全&from_source=banner_search&duration=1&spm_id_from=333.334.b_62616e6e65725f6c696e6b.1&page='
    page_url = root_url+str(index)
    html = requests.get(page_url,headers = headers)
    html.encoding = 'utf-8'  # 解决中文乱码
    soup = BeautifulSoup(html.text, 'lxml')
    av_list = []
    videos = soup.find_all('span', attrs={'class': 'type avid'})
    for v in videos:
        av_list.append(v.text[2:])  #截取字符串第三位到末尾
    return av_list

def get_video_info(aid):
    """
    根据av号返回视频的信息
    :param aid: av号
    :return:
    """
    video_url = 'https://www.bilibili.com/video/av'+str(aid)  # 视频链接
    target_url = "http://api.bilibili.com/playurl?callback=callbackfunction&aid=" + str(aid) + "&page=1&platform=html5&quality=1&vtype=mp4"  # json链接
    json_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)

    html = requests.get(video_url, headers = headers)
    html.encoding = 'utf-8'  # 解决中文乱码
    soup = BeautifulSoup(html.text, 'lxml')
    title = soup.find('meta', attrs={'itemprop': 'description'}).get('content')
    author = soup.find('meta', attrs={'itemprop': 'author'}).get('content')
    pubdate = soup.find('meta', attrs={'itemprop': 'datePublished'}).get('content')
    comment = soup.find('meta', attrs={'itemprop': 'commentCount'}).get('content')
    source_url = get_source_url(target_url)
    video_info = dict()
    video_info['title'] = title
    video_info['author'] = author
    video_info['pubdate'] = pubdate
    video_info['video_url'] = video_url
    video_info['source_url'] = source_url
    video_info['aid'] = aid
    video_info['comment'] = comment

    # 添加like和collect数据
    json_html = requests.get(json_url, headers = headers)
    json_result = json_html.text
    json_obj = json.loads(json_result)
    if json_obj:
        data = json_obj.get('data')
        stat = data.get('stat')
        video_info['like'] = stat.get('like')
        video_info['collect'] = stat.get('favorite')

    print(video_info)
    return video_info

def get_source_url(url):
    """
    根据视频json链接获取视频源链接
    cookie可能会过期
    :param url: json链接
    :return:
    """
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("UM_distinctid", "1699fc8a803cc-012a4263fbe9ed-9333061-100200-1699fc8a804192")
    cookie_jar.set("buvid3", "0C3077B9-8A50-4A04-88A0-35FE17ECBDC049014infoc")
    # cookie = "buvid3=0C3077B9-8A50-4A04-88A0-35FE17ECBDC049014infoc; LIVE_BUVID=AUTO9515531586306846; stardustvideo=1; CURRENT_FNVAL=16; sid=9gwiy9iv; rpdid=kklxplmqsidosskosloxw; UM_distinctid=1699fc8a803cc-012a4263fbe9ed-9333061-100200-1699fc8a804192; stardustpgcv=0606; arrange=list; _dfcaptcha=92d7ce3114dd9a520f59422c675ffdf9; fts=1554430452"
    json_str = requests.get(url, headers=headers, cookies=cookie_jar)
    result = json_str.text
    json_obj = json.loads(result)
    if json_obj:
        durl = json_obj.get('durl')
        if durl:
            video_url = durl[0]['url']
            return video_url
    return None


def spider_bili(dirname, begin, end):
    """
    爬取哔哩哔哩视频，下载视频并将视频信息存入数据库
    :param begin: 起始页码
    :param end: 终止页码
    :return:
    """
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.bilibili  # 连接mydb数据库，没有则自动创建
    my_set = db.videoinfo  # 使用newspeople集合，没有则自动创建

    for index in range(begin, end+1):    #遍历页数
        print('开始爬取第' + str(index) + '页视频')
        av_list = get_av_list(index)
        for aid in av_list: #遍历av_list
            #print(aid)
            video_info = get_video_info(aid)    #获取视频信息
            if '2018' not in video_info['pubdate']:
                continue
            my_set.insert(video_info)   #插入数据库
            download_video(dirname, aid, video_info['source_url']) #下载视频


def download_video(target_directory, aid, url):
    """
    下载视频
    :param target_directory: 存储视频的文件夹
    :param aid: 视频av号
    :param url: 视频源链接
    :return:
    """
    print('开始下载'+str(aid))
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    filename = str(aid)+'.mp4'
    filepath = os.path.join(target_directory, filename)
    # 二进制写入
    with open(filepath, 'wb') as f:
        try:
            video = requests.get(url, headers=headers, stream=True)
        except requests.exceptions.ConnectionError as e:
            print("连接失败" + str(e.message))
        except error.HTTPError as e:
            print('http请求错误:' + str(e.message))
        else:
            if video.status_code == 200:
                print(video.headers)
                size = int(video.headers['content-length'])
                print(size)
                t = tqdm.tqdm(total=size)
                for chunk in video.iter_content(1024):
                    f.write(chunk)
                    t.update(len(chunk))
                t.close()



if __name__ == '__main__':
    spider_bili('mp4_videos', 1, 50)
   
    