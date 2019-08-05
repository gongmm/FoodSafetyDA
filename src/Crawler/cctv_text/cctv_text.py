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
    'User-Agent': random.choice(UA_LIST)
}

des_dir = 'csv'
csv_name = 'cctv_text.csv'
browser = webdriver.Chrome()


def spider_food(begin, end):
    """
    根据页码进行食品安全关键词下的爬虫
    :param begin:
    :param end:
    :return:
    """

    # 判定csv文件是否存在，并写入headers
    if des_dir not in os.listdir():
        os.mkdir(des_dir)
    path = os.path.join(des_dir, csv_name)
    headers = ['title', 'pubdate', 'url', 'content']
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)


    food_url = 'https://search.cctv.com/search.php?qtext=食品安全&sort=relevance&type=web&vtime=&datepid=1&channel=&page='
    news_list = []
    for i in range(begin, end+1):
        print('____爬取第'+str(i)+'页____')
        url = food_url+str(i)
        news_url = get_news_url(url)
        for news in news_url:
            news_info = get_content(news)
            if news_info:
                news_list.append(news_info)
        save_file(path, news_list)
        news_list = []



def get_news_url(page_url):
    """
    获取每一页的新闻链接
    :param page_url: 页码链接
    :return: news_url：新闻链接list
    """
    browser.get(page_url)
    # html = requests.get(page_url,headers=headers)
    # print(html.text)
    html_doc = browser.page_source
    #print(html_doc)
    soup = BeautifulSoup(html_doc,'lxml')
    news_urls = []

    news_div = soup.find('div',attrs={'class':'outer'})
    news = news_div.find_all('li')
    #print(news)

    for li in news:
        #print(li.find('span').get('lanmu1'))
        news_urls.append(li.find('span').get('lanmu1'))
    time.sleep(0.5)
    return news_urls

def get_content(news_url):
    """
    根据新闻链接获取新闻内容
    :param news_url: 新闻原链接
    :return: news_info：新闻信息，dict类型
    """
    print(news_url)
    news_info = dict()  # 存储新闻内容
    # html = requests.get(news_url, headers=headers)
    browser.get(news_url)
    html = browser.page_source
    # html.encoding = 'utf-8'  # 解决中文乱码
    soup = BeautifulSoup(html, 'lxml')
    url = news_url
    title = soup.find('title').text
    keyword = soup.find('meta',attrs={'name':'keywords'}).get('content')

    # if soup.find('span',attrs={'class':'info'}):
    try:
        pubdtae = soup.find('span', attrs={'class': 'info'}).find('i').text.split(' ')[1]
        # p_list = soup.find_all('p',attrs={'style':'text-indent: 2em;'})
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




def save_file(filename, news_list):
    """
    将爬取到的新闻存入csv文件
    :param filename:
    :param news_list:
    :return:
    """
    with open(filename, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for news in news_list:
            writer.writerow([news['title'], news['pubdate'], news['url'], news['content']])
        print('成功保存至csv文件！')


if __name__ == '__main__':
    spider_food(1, 50)  # 50页之后都是重复