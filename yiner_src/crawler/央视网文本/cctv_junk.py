import json
import random
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import tqdm
import os
import csv
import pandas as pd
from selenium import webdriver
from pymongo import MongoClient
import jsonpath

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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST),

}


def spider():
    category_url = ['http://news.cctv.com/china/data/index.json',
                    ' http://news.cctv.com/world/data/index.json',
                    'http://military.cctv.com/data/index.json',
                    'http://news.cctv.com/tech/data/index.json',
                    'http://news.cctv.com/society/data/index.json',
                    ' http://news.cctv.com/law/data/index.json',
                    'http://news.cctv.com/ent/data/index.json',
                    ' http://jingji.cctv.com/data/index.json']

    conn = MongoClient('127.0.0.1', 27017)
    db = conn.cctv  # 连接mydb数据库，没有则自动创建
    my_set = db.junknews  # 使用newspeople集合，没有则自动创建

    for i,category in enumerate(category_url):
        print('第'+str(i)+'类______'+category+'______')
        #print(category)
        url_list = get_news_url(category)
        news_list = []
        for url in url_list:
            news_info = get_content(url)
            if news_info:
                news_list.append(news_info)
        my_set.insert(news_list)

def get_news_url(class_url):
    """
    获取当前类别的新闻链接
    :param class_url: 不同分类的初始链接
    :return: news_url：新闻链接list
    """
    html = requests.get(class_url,headers=headers)
    html.encoding='utf-8'
    json_html = json.loads(html.text)
    url_list = jsonpath.jsonpath(json_html,'$..url')

    # for title in title_list:
    #     print(title)
    return url_list


def get_content(news_url):
    """
    根据新闻链接获取新闻内容
    :param news_url: 新闻原链接
    :return: news_info：新闻信息，dict类型
    """
    print(news_url)
    news_info = dict()  #存储新闻内容
    html = requests.get(news_url,headers=headers)
    html.encoding = 'utf-8' #解决中文乱码
    soup = BeautifulSoup(html.text,'lxml')
    url = news_url
    title = soup.find('title').text
    keyword = soup.find('meta',attrs={'name':'keywords'}).get('content')


    #if soup.find('span',attrs={'class':'info'}):
    try:
        pubdtae = soup.find('span', attrs={'class': 'info'}).find('i').text.split(' ')[1]
        #p_list = soup.find_all('p',attrs={'style':'text-indent: 2em;'})
        p_list = soup.find_all('p')
        content = ''
        for p in p_list:
            content = content+p.text
        content = content.split('\n')[2]
        #print(content)

        news_info['title'] = title
        news_info['url'] = url
        news_info['keyword'] = keyword
        news_info['pubdate'] = pubdtae
        news_info['content'] = content

        time.sleep(0.5)
        return news_info
    except Exception as e:
        #print(e.message)
        return None




def save_file(filename,news_list):
    """
    将爬取到的新闻存入csv文件
    :param filename:
    :param news_list:
    :return:
    """
    with open(filename,'a') as f:
        writer = csv.writer(f)
        for news in news_list:
            writer.writerow([news['title'],news['pubdate'],news['url'],news['content']])


if __name__ == '__main__':
    # news_list = spider()
    # save_file('foodsafty.csv',news_list)
    #get_content('http://military.cctv.com/2019/03/25/ARTIb2vQqxr7dSRL7A7lcdMU190325.shtml?spm=C95414.PwcreT7zLCIH.S24711.3')
    #get_news_url('http://news.cctv.com/tech/data/index.json')
    spider()

