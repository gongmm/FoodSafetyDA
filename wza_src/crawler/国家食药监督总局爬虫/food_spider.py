# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import random
import json
import datetime
import requests
import csv

from bs4 import BeautifulSoup

from xml import etree
# from importlib import reload
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'samr.cfda.gov.cn',
    'Referer': 'http://samr.cfda.gov.cn/WS01/CL1029/index.html',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Cookie': 'FSSBBIl1UgzbN7N80S=qXFePHZLELjZSmqvSV1iqohoYD0eB8W.SLFTb3kfkvhD8CeG06CkANgxrvkOrrot; FSSBBIl1UgzbN7N80T=2Q4XUJgIvU9lGglmMxOkspy5514e7CShIBMI95zLRsjYj1D9XSmrHAN6bebTTi0pQLPqAq19W_X4IZsFGGpL.BojD7BRKi46ASkTODds3brbtO1K5X1oDhFYQP7lz2Y.IIDR8cu4Yfagb0XqGBsd1L47i1flhk6.a0VkVIhsgDqEUk525Ymysyy8raOVZATUPMX2ipbin9kek8P7aEgRVuKY.s6hMVgs6Jtia2oeGdVz0zgiUxJoCQ72Zk7FRyGnD17TzDAQAWUjDhHqcWxKgpDmoH19_G3whIqqSO0_PRonBfWOXV6mfCK88NWn_2T50xmd0Ep4kul_y3gfDWcuk1kAwFrbKbrWbl5a0USOqa66wra',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ximalaya.com/dq/all/2',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': 'FSSBBIl1UgzbN7N80S=qXFePHZLELjZSmqvSV1iqohoYD0eB8W.SLFTb3kfkvhD8CeG06CkANgxrvkOrrot; FSSBBIl1UgzbN7N80T=2Q4XUJgIvU9lGglmMxOkspy5514e7CShIBMI95zLRsjYj1D9XSmrHAN6bebTTi0pQLPqAq19W_X4IZsFGGpL.BojD7BRKi46ASkTODds3brbtO1K5X1oDhFYQP7lz2Y.IIDR8cu4Yfagb0XqGBsd1L47i1flhk6.a0VkVIhsgDqEUk525Ymysyy8raOVZATUPMX2ipbin9kek8P7aEgRVuKY.s6hMVgs6Jtia2oeGdVz0zgiUxJoCQ72Zk7FRyGnD17TzDAQAWUjDhHqcWxKgpDmoH19_G3whIqqSO0_PRonBfWOXV6mfCK88NWn_2T50xmd0Ep4kul_y3gfDWcuk1kAwFrbKbrWbl5a0USOqa66wra',
    # 'User-Agent': random.choice(UA_LIST)
}

browser = webdriver.Chrome()

base_url = "http://samr.cfda.gov.cn/WS01"
src_url = base_url + "/CL1972/index.html"


def get_url(url, last_href):
    browser.get(url)
    time.sleep(3)
    html_doc = browser.page_source

    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    td_elements = soup.find_all('td', class_="ListColumnClass15")
    info_list = []

    next_href = soup.find('td', class_="pageTdE15").find('a').get('href')

    for item in td_elements:
        info = {}

        info['title'] = item.find('a').getText().strip()
        info['href'] = base_url + item.find('a').get('href')[2:]
        info['time'] = item.find('span').getText()[1:-2]

        # link = browser.find_element_by_link_text(info['title'])
        # link.click()
        browser.get(info['href'])
        time.sleep(3)
        new_html_doc = browser.page_source
        # print(new_html_doc)
        # print(new_html_doc.decode("utf8","ignore").encode("gbk","ignore"))
        soup2 = BeautifulSoup(str(new_html_doc), 'html.parser', from_encoding='utf-8')

        temp = soup2.find('td', class_='articlecontent3')
        if temp:
            # 消除html中特殊的转义字符
            content = temp.getText()
            info['content'] = "".join(content.split())
        #print(type(content))
        #print(content)
        else:
            info['content'] = ''
        browser.back()
        info_list.append(info)

    write2csv(info_list, "xuanchuanzhengzhi.csv")
    if next_href != last_href:
        next_page_src = src_url[:src_url.rfind('/') + 1] + next_href
        print(next_page_src)
        # go_next_page()
        time.sleep(3)
        #print(next_page_src)
        get_url(next_page_src, next_href)


def go_next_page():
    # 下一页按钮
    link = browser.find_element_by_link_text("下一页")
    print(link)
    link.click()


def write2csv(info_list, out_file):
    with open(out_file, 'a', newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        fields = info_list[0].keys()  #
        fields = sorted(list(fields))
        #print(info_list)
        # w.writerow(fields)
        for item in info_list:
            w.writerow([item[field] for field in fields])


if __name__ == '__main__':
    get_url(src_url, "end")