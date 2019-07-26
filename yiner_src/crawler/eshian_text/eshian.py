import json
import random
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import tqdm
import os
import csv
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By

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

base_url = "http://www.eshian.com"
download_baseurl = "http://www.eshian.com/sat/standard/standardinfodown/"

page_url = 'http://www.eshian.com/sat/foodinformation/hync/articlelist/17/453/1'

#chrome_driver = '/Users/yiner/anaconda3/lib/python3.6/site-packages/selenium/webdriver/chrome/chromedriver'
#browser = webdriver.Chrome(executable_path=chrome_driver)
#option = webdriver.ChromeOptions()
#option.add_argument('--proxy=49.86.182.111:9999')
#option.add_argument('--proxy-server=http://27.208.29.151:8060')
#option.add_argument('--proxy-type=http')
#browser = webdriver.Chrome(options=option)

def get_ip_list(path):
    with open(path, 'r') as f:
        proxies_list = f.readlines()
        return proxies_list

ip_list = get_ip_list('proxy.txt')
index = 0  

def get_ip():
    global index
    proxy_ip = 'https://' + ip_list[index][:-1]
    proxies = {'https': proxy_ip}
    index = (index+1) % len(ip_list)
    return proxies

proxies = get_ip()

def get_item_url(pagenum):
    """
    根据页码爬取该页面下的所有item的url链接
    :param pagenum:
    :return:
    """
    # page_html = browser.get(page_url)
    # input_str = browser.find_element_by_id('_paging_ingput_value_')
    # input_str.clear()
    # input_str.send_keys(pagenum)
    # time.sleep(0.5)
    # button = browser.find_element_by_id('gotoPage')
    # button.click()
    
    # try:
    #     #最多等待10秒
    #     locator = (By.ID, '_paging_ingput_value_')
    #     WebDriverWait(browser, 10).until(
    #         expected_conditions.visibility_of_element_located(locator))

    #     date = browser.find_elements_by_css_selector('span.pull-right').pop(-1).text
    #     if '2018' not in date:
    #         return []
    #     url_list = []
    #     #soup = BeautifulSoup(page_html.text, 'lxml')

    #     # for item in soup.select('ul.article-tab-list > li'):
    #     #     href = item.find('a').get('href')
    #     #     #print(href)
    #     #     url_list.append(base_url + href)

    #     for item in browser.find_elements_by_css_selector('ul.article-tab-list > li'):
    #         href = item.find_element_by_css_selector('a').get_attribute('href')
    #         #print(href)
    #         url_list.append(href)

    #     return url_list
    # except Exception as e:
    #     print(e)
    #     print("Can't find page")
    #     return []

    times = 1
    while True:
        try:
            global proxies
            if times>=2:
                proxies = get_ip()
                print('已重新获取ip\n', proxies)
            print('正在获取列表页面...')
            print(proxies)
            html = requests.post(page_url, headers=headers1, data={'pageNo':str(pagenum-1)}, proxies=proxies, timeout=5)
            soup = BeautifulSoup(html.text,'lxml')
            last_date = soup.select('span.pull-right')[-1].text
            if '2018' not in last_date:  # 筛选2018年的
                return []

            url_list = []
            for item in soup.select('ul.article-tab-list > li'):
                href = item.find('a').get('href')
                #print(href)
                url_list.append(base_url + href)
            return url_list
        except requests.exceptions.ConnectTimeout as e:
            print(e)
            print('请求超时！')
            times += 1
        finally:
            if times >=7:
                print('无法请求页面！')
                return []


def get_iteminfo(url):
    """
    爬取新闻文本
    :param url:新闻网页链接
    :return: item_info: dict()，新闻信息
    """
    item_info = dict()
    
    times = 1
    while True:
        try:
            global proxies
            if times%2 == 0:
                proxies = get_ip()
                print('已重新获取ip')
            print('正在获取新闻页面...')
            html = requests.get(url, headers=headers1, proxies=proxies, timeout=5)
            soup = BeautifulSoup(html.text,'lxml')
            if not soup.find(class_='text-success'):
            	continue
            title = soup.find(class_='text-success').text
            pubdate = soup.select('.article-subtitle > span')[1].select('em')[0].text.strip()
            if '2018' not in pubdate:  # 筛选2018年的
                return None
            viewCount = soup.select('.article-subtitle > span')[2].select('em')[0].text
            content = soup.select('.new-article')[0].get_text()
            item_info['title'] = title
            item_info['pubdate'] = pubdate
            item_info['viewCount'] = viewCount
            item_info['url'] = url
            item_info['content'] = content
            print(item_info)
            return item_info
        except requests.exceptions.ConnectTimeout as e:
            print(e)
            print('请求超时！')
            times += 1
            time.sleep()
        finally:
            if times >=7:
                print('无法请求页面！')
                return None

    

def spider(page_begin, page_end):
    """
    爬虫
    :param page_begin: 起始pagenum
    :param page_end: 结束pagenum
    :return:
    """
    food_news = []
    des_dir = 'csv'
    csv_name = 'eshian_text.csv'
    write_header_2csv(des_dir, csv_name)
    for i in range(page_begin,page_end):
        print(i)
        print('_______第'+str(i)+'页________')
        urls = get_item_url(i)
        for j in range(len(urls)):
            print(urls[j])
            item_info = get_iteminfo(urls[j])
            time.sleep(5)
            if item_info:
                food_news.append(item_info)
        if food_news:
            write2csv(food_news, des_dir, csv_name)
        food_news = []

def write_header_2csv(des_dir, csv_name):
    if des_dir not in os.listdir():
        os.mkdir(des_dir)
    path = os.path.join(des_dir, csv_name)
    headers = ['title', 'pubdate', 'viewCount', 'url', 'content']
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(headers)


def write2csv(food_news, des_dir, csv_name):
	if des_dir not in os.listdir():
		os.mkdir(des_dir)
	path = os.path.join(des_dir, csv_name)
	with open(path, 'a', newline='', encoding='utf-8') as f:
		w = csv.writer(f)
		for news in food_news:
			w.writerow(list(news.values()))
	print('成功写入csv文件！')



if __name__ == '__main__':
    food_news = spider(40, 80)