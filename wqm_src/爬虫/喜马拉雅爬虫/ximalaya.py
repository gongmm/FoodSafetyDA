import json
import random
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import tqdm
import os
import csv
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
headers1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST)
}
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ximalaya.com/dq/all/2',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST)
}

conn = MongoClient('127.0.0.1', 27017)
db = conn.ximalaya  # 连接mydb数据库，没有则自动创建
my_set = db.fminfo  # 使用newspeople集合，没有则自动创建

base_url = "https://www.ximalaya.com"
def get_fm_urls(pagenum):
    """
    获取查到的食品这一页的音频url，
    Params:
        pagenum: int, 页码
    Return:
        urls: list, url列表
    """
    fm_list_url = "https://www.ximalaya.com/search/album/食品/sc/p" + str(pagenum)
    print(fm_list_url)
    html = requests.get(fm_list_url, headers=headers1)
    # print(html.text)
    url_list = []
    soup = BeautifulSoup(html.text, 'lxml')
    for item in soup.find_all(class_="xm-album-cover"):
        href = item.get('href')
        url_list.append(base_url + href)
    return url_list

def get_audio_url(url):
    """
    获取某一内容下的所有音频资源
    Params:
        url: str, 内容url
    Return:
        audio_urls: list, 音频urls,包括 专辑名，音频名，url
    """
    # url = "https://www.ximalaya.com/jiaoyu/15362520/"
    print(url)
    html = requests.get(url, headers=headers1)
    audio_infos = []
    
    soup = BeautifulSoup(html.text, 'lxml')
    album = soup.find("h1", class_="title _t4_").getText()
    update_time = soup.find("span", class_="time _t4_").getText()
    for item in soup.find_all("div", class_="text _OO"):
        href = item.find('a').get('href')
        dic = dict()
        dic['href'] = base_url + href
        dic['title'] = album + '_' + item.find('a').get('title')
        # dic['album'] = album
        # dic['update_time'] = update_time
        audio_infos.append(dic)
    # print(audio_infos)
    return audio_infos

def write2csv(audio_info_list, out_file):
    with open(out_file, 'a', newline='') as f:
        w = csv.writer(f)
        # fields=audio_info_list[0].keys()  #
        for audio_info in audio_info_list:
            w.writerow([audio_info['href'], audio_info['source_url'], audio_info['update_time'], audio_info['title'], audio_info['content']])



def save_audio_info( audio_infos):
    """
    保存信息到数据库
    """
    print
    bad_index = []
    for index in range(len(audio_infos)):
        # 音频网页链接
        url = audio_infos[index]['href']
        num = url[url.rfind('/')+1:]
        target_url = "http://www.ximalaya.com/tracks/" + num + ".json"
        html = requests.get(target_url, headers=headers1).text
        dic = json.loads(html)
        # 音频链接地址
        if 'play_path_64' in dic:
            source_url = dic['play_path_64']
        else:
            bad_index.append(index)
            continue
        html = requests.get(url, headers=headers1).text
        soup = BeautifulSoup(html, 'lxml')
        update_time = soup.find("span", class_="time _zMC").getText()
        item = soup.find("div", class_="to-seo hidden _zMC")
        audio_infos[index]['content'] = ""
        if item:
            content = item.contents
            if len(content) >= 3:
                audio_infos[index]['content'] = content[2]
        audio_infos[index]['source_url'] = source_url
        audio_infos[index]['update_time'] = update_time

    # 倒序删除list元素
    for bad in sorted(bad_index, reverse=True):
        del audio_infos[bad]
    print(audio_infos)
    my_set.insert(audio_infos)

    #write2csv(audio_infos, os.path.join(target_directory, filename))


def download_audio(target_directory, url,filename):
    """
    下载音频
    Params:
        target_directory: 存储的目标文件夹位置
        url: 音频url
    Return:
        None
    """
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    num = url[url.rfind('/')+1:]
    target_url = "http://www.ximalaya.com/tracks/" + num + ".json"
    html = requests.get(target_url, headers=headers1).text
    dic = json.loads(html)
    # 音频链接地址
    path = dic['play_path_64']
    #filename = path[path.rfind('/')+1:]
    # 二进制写入
    with open(target_directory+'/'+filename, 'wb') as f:
        try:
            audio = requests.get(path, headers=headers1, stream=True)
        except exceptions.ConnectionError as e:
            print("连接失败" + str(e.message))
        except exceptions.HTTPError as e:
            print('http请求错误:' + str(e.message))
        else:
            if audio.status_code == 200:
                size = int(audio.headers['content-length'])
                print(size)
                t = tqdm.tqdm(total=size)
                for chunk in audio.iter_content(1024):
                    f.write(chunk)
                    t.update(len(chunk))
                t.close()

def ximalaya_spider(dirname,begin,end):
    for index in range(begin,end+1):
        print('开始爬取第'+str(index)+'页的音频')
        url_list = get_fm_urls(index)
        #print("start")
        # 遍历专辑
        for url in url_list:
            audio_urls = get_audio_url(url)
            # 保存数据
            save_audio_info(audio_urls) #存储数据库
            for audio_url in audio_urls:
                download_audio(dirname,audio_url['href'],audio_url['title'])  #下载音频文件
            #print("save one record")
        print("---------------------")

if __name__ == '__main__':
    ximalaya_spider('爬虫/喜马拉雅爬虫/ximalaya_fm',1,2)