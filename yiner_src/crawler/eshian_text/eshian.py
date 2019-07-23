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

base_url = "http://www.eshian.com"
download_baseurl = "http://www.eshian.com/sat/standard/standardinfodown/"

url_begin = "http://www.eshian.com/sat/standard/standardlist/0?info=&pageNo="
url_end="&type=8&standardStatus=8"

conn = MongoClient('127.0.0.1', 27017)
db = conn.shiantong  # 连接mydb数据库，没有则自动创建
my_set = db.newsinfo  # 使用newspeople集合，没有则自动创建

def get_item_url(pagenum):
    """
    根据页码爬取该页面下的所有item的url链接
    :param pagenum:
    :return:
    """
    from_url = url_begin+str(pagenum)+url_end   #爬取的页面url
    html = requests.get(from_url, headers=headers1)
    url_list = []
    soup = BeautifulSoup(html.text, 'lxml')
    for item in soup.find_all(class_="text-default"):
        href = item.find('a').get('href')
        #print(href)
        url_list.append(base_url + href)
    return url_list


def get_iteminfo(url):
    """
    爬取该标准的名称，若有源pdf文件则给出下载链接
    :param url:标准网页链接
    :return: item_info: dict()，标准信息
    """
    item_info = dict()
    html = requests.get(url,headers=headers1)
    soup = BeautifulSoup(html.text,'lxml')
    title = soup.find('title').text
    item_info['title'] = title
    item_info['url'] = url
    #print(title)
    down_btn = len(soup.find_all(class_='btn btn-file'))
    if down_btn==3:
        num = url.split('/')[4].split('.')[0]
        download_url = download_baseurl+num
        item_info['download_url'] = download_url
        #print(download_url)
    else:
        item_info['download_url'] = ''
        #print('无原pdf可下载')

    #print(item_info)
    return item_info

def spider(page_begin,page_end):
    """
    爬虫
    :param page_begin: 起始pagenum
    :param page_end: 结束pagenum
    :param filename: 保存结果文件路径
    :return:
    """
    standards = []
    for i in range(page_begin,page_end):
        print(i)
        print('_______第'+str(i)+'页________')
        urls = get_item_url(i)
        for j in range(len(urls)):
            print(urls[j])
            item_info = get_iteminfo(urls[j])
            my_set.insert(item_info)
    #         standards.append(item_info)
    #
    #     #将标准信息写入csv文件
    #     with open(filename, 'a') as f:
    #         w = csv.writer(f)
    #         for standard in standards:
    #             w.writerow([standard['title'], standard['url'], standard['download_url']])
    # return standards

def write2csv(standards,filename):
    with open(filename,'a') as f:
        w = csv.writer(f)
        for standard in standards:
            w.writerow([standard['title'],standard['url'],standard['download_url']])



if __name__ == '__main__':
    #get_item_url(1)
    #get_iteminfo("http://www.eshian.com/standards/13801.html")
    standards = spider(1,10)
    #write2csv(standards,'result.csv')
    