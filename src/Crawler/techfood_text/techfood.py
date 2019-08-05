import random
import time
import requests
from bs4 import BeautifulSoup
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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST),
}

base_url = "https://www.tech-food.com/news/detail/n"

def get_ip_list(path):
    with open(path, 'r') as f:
        proxies_list = f.readlines()
        return proxies_list

ip_list = get_ip_list('proxy1.txt')
index = 0

def get_ip():
    global index
    proxy_ip = 'http://' + ip_list[index][:-1]
    proxies = {'http': proxy_ip}
    index = (index+1) % len(ip_list)
    return proxies

proxies = get_ip()

def get_content(news_url):
    """
    根据新闻链接获取新闻内容
    :param news_url: 新闻原链接
    :return: news_info：新闻信息，dict类型
    """
    print(news_url)
    news_info = dict()  # 存储新闻内容
    times = 1
    while True:
        try:
            global proxies
            if times >= 2:
                proxies = get_ip()
                print('已重新获取ip\n', proxies)
            html = requests.get(news_url, headers=headers, verify=False, proxies=proxies, timeout=5)
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')

            any_div = soup.find('div')
            if not any_div:  # 网页没加载出来则重新加载
                times += 1
                if times >= 5:
                    print('无法加载页面！')
                    return None
                print('重新加载页面...')
                continue

            # 找到导航栏中栏目为食品安全的网页，非食品安全的跳过
            navi_div = soup.find('div', attrs={'id': 'daohan_l'})
            if not navi_div:  # 网页404
                return None
            navi = navi_div.find_all('a')[2].text
            if not navi == '食品安全':
                print('不属于食品安全栏目')
                return None

            print('属于食品安全栏目')
            title = soup.find(class_='biaoti1').text
            pub = soup.find(class_='biaoti1x').text
            pubdate = (pub.split()[0]).split('：')[1]

            tag_p = soup.find('div', attrs={'id': 'zoom'}).find_all('p')
            content = ''
            for p in tag_p:
                content = content + p.text

            news_info['title'] = title
            news_info['pubdate'] = pubdate
            news_info['url'] = news_url
            news_info['content'] = content
            return news_info
        except Exception as e:
            print(e)
            print('请求超时！')
            times += 1
        finally:
            if times >= 7:
                print('无法请求页面！')
                return None


def spider():
    print('——————开始爬取食品科技网的资讯——————')
    food_news = []
    des_dir = 'csv'
    csv_name = 'techfood_text.csv'
    write_header_2csv(des_dir, csv_name)

    # 1377421
    # 1378035, 1378061
    # 1379705
    # 1380876, 1380881
    # 1400458, 1400459
    # 1405000, 1410000 yiner
    # 1410000, 1415411 zang
    for i in range(1400459, 1405000):  # 从1376251到1415410为2018年所有资讯
        print('——————开始爬取第%d个网页——————' % i)
        news_url = base_url + str(i) + '.htm'
        news_info = get_content(news_url)
        if news_info:
            food_news.append(news_info)
            if len(food_news) % 10 == 0 or i == 1415410:
                write2csv(food_news, des_dir, csv_name)
                food_news = []
        time.sleep(2)
        print('——————结束爬取——————')

    print('——————————完成——————————')


def write_header_2csv(des_dir, csv_name):
    if des_dir not in os.listdir():
        os.mkdir(des_dir)
    path = os.path.join(des_dir, csv_name)
    header = ['title', 'pubdate', 'url', 'content']
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)


def write2csv(food_news, des_dir, csv_name):
    if des_dir not in os.listdir():
        os.mkdir(des_dir)
    path = os.path.join(des_dir, csv_name)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        for news_info in food_news:
            w.writerow([news_info['title'], news_info['pubdate'],
                        news_info['url'], news_info['content']])
    print('成功写入csv文件！')


if __name__ == '__main__':
    spider()
