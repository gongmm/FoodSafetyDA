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
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST),

}


root_url1 = "https://www.tech-food.com/news/c15/list_"
root_url2 = "https://www.tech-food.com/news/c17/list_"
base_url = "https://www.tech-food.com"

def get_page_url():
    """
    100页的网页链接
    :return:
    """
    url_list = []
    for i in range(1,101):
        page_url = root_url1+str(i)+'.html'
        url_list.append(page_url)
    for i in range(1,101):
        page_url = root_url2+str(i)+'.html'
        url_list.append(page_url)
    return url_list

def get_news_url(page_url):
    """
    获取每一页的新闻链接
    :param page_url: 页码链接
    :return: news_url：新闻链接list
    """
    print(page_url)
    html = requests.get(page_url,headers=headers)
    soup = BeautifulSoup(html.text,'lxml')
    news_urls = []
    td = soup.find_all(class_='titleTxt')
    for t in td:
        url = base_url + t.find('a').get('href')
        news_urls.append(url)

    time.sleep(0.5)
    return news_urls

def get_content(news_url):
    """
    根据新闻链接获取新闻内容
    :param news_url: 新闻原链接
    :return: news_info：新闻信息，dict类型
    """
    print(news_url)
    news_info = dict()  #存储新闻内容
    html = requests.get(news_url,headers=headers)
    soup = BeautifulSoup(html.text,'lxml')
    url = news_url
    title = soup.find(class_='biaoti1').text
    #print(title)
    pub = soup.find(class_='biaoti1x').text
    pubdate = (pub.split(' ')[0]).split('：')[1]
    #print(pubdate)

    tag_p = soup.find('div',attrs={'id':'zoom'}).find_all('p')
    content = ''
    for p in tag_p:
        content = content+p.text
    #print(content)

    news_info['title'] = title
    news_info['pubdate'] = pubdate
    news_info['url'] = url
    news_info['content'] = content

    time.sleep(0.5)
    return news_info

# def spider(filename):
#
#     url_list = get_page_url()
#     with open (filename,'a') as f:
#         writer = csv.writer(f)
#         for page in url_list:
#             news_urls = get_news_url(page)
#             for news in news_urls:
#                 news_info = get_content(news)
#
#                 writer.writerow([news_info['title'],news_info['pubdate'],news_info['url'],news_info['content']])

def spider():
    url_list = get_page_url()
    for page in url_list:
        news_urls = get_news_url(page)
        for news in news_urls:
            news_info = get_content(news)
            insert_mongodb(news_info)

def insert_mongodb(news_info):
    print('插入数据库')
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.shipinkeji  # 连接mydb数据库，没有则自动创建
    my_set = db.newsinfo  # 使用newspeople集合，没有则自动创建
    my_set.insert(news_info)

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
            writer.writerow(news_list['title'],news_list['pubdate'],news_list['url'],news_list['content'])


if __name__ == '__main__':
    #get_news_url()
    #get_page_url()
    #get_content('https://www.tech-food.com/news/detail/n1421634.htm')
    spider()
