import json
import random
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import tqdm
import os
import csv

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

root_url = "http://www.cfsn.cn"


def get_category_url():
    """
    获取首页第一栏子类别的链接
    :return: category_urls，链接list
    """
    html = requests.get(root_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    category_urls = []

    # 第一栏
    class_nav = soup.find(class_='nav')
    i = 0
    for a in class_nav.find_all('a'):
        if i == 0:  # 跳过第一个url（首页）
            i += 1
            continue
        url = a.get('href')
        # print(url)
        category_urls.append(url)  # 将其他类的url存入list
        i += 1

    # 第二栏
    class_list = soup.find(class_='wal subNav').find(class_='list')
    i = 0
    for a in class_list.find_all('a'):
        i += 1
        if i == 9 or i == 10:  # 过滤掉地方和企业版块（不同）
            continue
        url = a.get('href')
        # print(url)
        category_urls.append(url)

    # for url in category_urls:
    #     print(url)
    return category_urls


def get_page_url(category_url):
    """
    每一类别下有几页，获取每一页的链接
    :param category_url: 每个栏目的链接
    :return: page_urls：几页的链接list
    """
    html = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    page_urls = []
    pageNum = soup.find(class_='pageNum')
    if pageNum is None:
        return page_urls
    tag_a = pageNum.find_all('a')
    # print(len(tag_a))
    for i in range(1, len(tag_a) - 1):
        url = tag_a[i].get('href')
        page_urls.append(url)
        # print(url)
    time.sleep(0.5)
    return page_urls


def get_news_url(page_url):
    """
    获取每一页的新闻链接
    :param page_url: 页码链接
    :return: news_url：新闻链接list
    """
    html = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    news_urls = []
    class_pagelist = soup.find(class_='pageList')
    pg_tag_a = class_pagelist.find_all('a')
    for a in pg_tag_a:
        url = a.get('href')
        # print(url)
        news_urls.append(url)
    time.sleep(0.5)
    return news_urls


def get_content(news_url):
    """
    根据新闻链接获取新闻内容
    :param news_url: 新闻原链接
    :return: news_info：新闻信息，dict类型
    """
    news_info = dict()  # 存储新闻内容
    html = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    url = news_url
    title = soup.find(class_='title').text
    pubdate = soup.find(class_='msg').find('div').contents[0]
    tag_p = soup.find(class_='content').find_all('p')
    content = ''
    for p in tag_p:
        p_content = p.text
        content = content + p_content

    news_info['title'] = title
    news_info['pubdate'] = pubdate
    news_info['url'] = url
    news_info['content'] = content

    time.sleep(0.5)
    return news_info


def spider():
    """
    爬取首页各个类别下的所有新闻
    :return: news_list：list，所有新闻的信息
    """
    news_list = []
    category_urls = get_category_url()  # 获取所有类别的链接
    for category in category_urls:
        print('______新类别_______')
        print(category)
        page_urls = get_page_url(category)  # 获取每一页的页面链接
        for page in page_urls:
            news_url = get_news_url(page)  # 获取每一页下的新闻链接
            for news in news_url:
                news_info = get_content(news)
                if "2018-01-01 00:00" < news_info['pubdate'] < "2019-01-01 00:00":
                    print(news_info)
                    news_list.append(news_info)
                else:
                    pass
        save_file('cfsn_news.csv', news_list)
        # 清空
        news_list = []


def save_file(filename, news_list):
    """
    将爬取到的新闻存入csv文件
    :param filename:
    :param news_list:
    :return:
    """
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        for news in news_list:
            writer.writerow([news['title'], news['pubdate'], news['url'], news['content']])


if __name__ == '__main__':
    spider()

    # get_category_url()
    # get_page_url('http://www.cfsn.cn/front/web/site.hangye?hyid=1&page=1')
    # get_content('http://www.cfsn.cn/front/web/site.newshow?hyid=1&newsid=932')
