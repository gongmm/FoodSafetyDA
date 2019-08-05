# -*-coding:utf-8-*-
from selenium import webdriver
from lxml import etree
import requests
import random
import csv
import re
import time

# import BeautifulSoup

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

allow_domain = 'http://bbs.foodmate.net/'


def parse_search_page():
    keyword = '非洲猪瘟'
    browser = webdriver.Chrome()
    browser.get('http://bbs.foodmate.net/search.php?')
    # 输入搜索内容
    input_key = browser.find_element_by_id('scform_srchtxt')
    input_key.clear()
    input_key.send_keys(keyword)
    button = browser.find_element_by_id('scform_submit')
    button.click()
    # h2=browser.window_handles
    # browser.switch_to.window(h2[1])
    # 获得搜索结果
    sel = etree.HTML(browser.page_source)
    print("====== Crawling Page: " + str(1) + "========")
    page_num = len(sel.xpath("//div[@class='pg']/a"))

    div_content = sel.xpath('//div[@id="threadlist"]//h3')
    items = []
    for index, ul_content in enumerate(div_content):
        print("====== Crawling Item: " + str(index) + "========")
        # for index in range(len(div_content)):
        #     ul_content = div_content[index]
        title = ul_content.xpath(".//a/text()")
        titles = ''
        for i in title:
            titles = titles + i
        print(titles)
        url = ul_content.xpath(".//a/@href")[0]
        print(url)
        pub_date = ul_content.xpath('../p[3]/span[1]/text()')[0]
        reply_num = re.findall('\d+', str(ul_content.xpath('../p[1]/text()')[0]))[0]
        read_num = re.findall('\d+', str(ul_content.xpath('../p[1]/text()')[0]))[1]
        '''存数据'''
        item = {}
        item['time'] = pub_date
        item['title'] = title
        item['reply_num'] = reply_num
        item['read_num'] = read_num
        if '2018-1-1' < pub_date < '2019-1-1':
            items.append(item)
        # print(time)
        # parse(url, titles, pub_date)
    if len(items) > 0:
        save('luntan.csv', items)
    # 是否存在下一页
    if sel.xpath("//div[@class='pg']"):
        next_page(sel.xpath("//div[@class='pg']/a/@href")[0])


def parse(url, title, pub_date):
    content_str = ""
    index = 0
    number = 0
    while True:
        index += 1
        # print("parse" + url)
        print("====== Crawling Topic Page: " + str(index) + "========")
        topic_per_page = requests.get(allow_domain + url, headers=headers)
        time.sleep(3)
        content_sel = etree.HTML(topic_per_page.text)
        contents = content_sel.xpath('//td[@class="t_f"]')
        for td_content in contents:
            review_list = td_content.xpath('.//text()')

            for review in review_list:
                remove_chars = '[0-9a-zA-Z’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
                content_str += re.sub(remove_chars, '', review).strip()
            content_str += '\n'
            number += 1
            # review = td_content.xpath('./td[@class="t_f"]')
        # print(content_str)
        if content_sel.xpath('//div[@class="pgbtn"]'):
            url = content_sel.xpath('//div[@class="pgbtn"]/a/@href')[0]
        else:
            break

    '''存数据'''
    item = {}
    item['time'] = pub_date
    item['title'] = title
    item['content'] = content_str
    item['number'] = number
    if '2018/01/01' < pub_date < '2019/01/01':
        save('luntan.csv', item)


def next_page(url):
    print("====== Crawling Page: " + url + "========")
    page_source = requests.get(allow_domain + url, headers=headers)
    sel = etree.HTML(page_source.text)
    div_content = sel.xpath('//div[@id="threadlist"]//h3')
    items = []
    for index, ul_content in enumerate(div_content):
        print("====== Crawling Item: " + str(index) + "========")
        # for index in range(len(div_content)):
        #     ul_content = div_content[index]
        title = ul_content.xpath(".//a/text()")
        titles = ''
        for i in title:
            titles = titles + i
        print(titles)
        url = ul_content.xpath(".//a/@href")[0]
        print(url)
        pub_date = ul_content.xpath('../p[3]/span[1]/text()')[0]
        reply_num = re.findall('\d+', str(ul_content.xpath('../p[1]/text()')[0]))[0]
        read_num = re.findall('\d+', str(ul_content.xpath('../p[1]/text()')[0]))[1]
        '''存数据'''
        item = {}
        item['time'] = pub_date
        item['title'] = title
        item['reply_num'] = reply_num
        item['read_num'] = read_num
        if '2018-1-1' < pub_date < '2019-1-1':
            items.append(item)
        # print(time)
        # parse(url, titles, pub_date)
    if len(items) > 0:
        save('luntan.csv', items)
    # 是否存在下一页
    if sel.xpath("//div[@class='pg']/a")[-1].text == '下一页':
        next_page(sel.xpath("//div[@class='pg']/a/@href")[-1])


def save(filename, items):
    with open(filename, 'a+', encoding='utf-8', newline='') as f:
        # f = open(filename,'a+',encoding='utf-8',newline = '')
        writer = csv.writer(f, dialect="excel")
        for item in items:
            writer.writerow([item['time'], item['title'], item['reply_num'], item['read_num']])


if __name__ == '__main__':
    parse_search_page()
