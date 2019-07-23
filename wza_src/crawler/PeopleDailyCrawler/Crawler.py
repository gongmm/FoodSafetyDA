import csv

from bs4 import BeautifulSoup

from Parser import Parser
import requests
import json
import time
import os

import math
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(r"user-data-dir=C:\Users\gnaiz\AppData\Local\Google\Chrome\User Data 2")
browser = webdriver.Chrome(chrome_options=option)

BaseUrl = "http://data.people.com.cn/sc/ss?qs="  # need to be change
SpecificBaseUrl = r"http://data.people.com.cn/sc/ss?qs="

GlobalJsonPart = {"clds": "23",
                  "cds":
                      [{"cdr": "AND",
                        "cds":
                            [{"fld": "title", "cdr": "OR", "hlt": "true", "vlr": "AND", "val": ""},
                             {"fld": "subTitle", "cdr": "OR", "hlt": "false", "vlr": "AND", "val": ""},
                             {"fld": "introTitle", "cdr": "OR", "hlt": "false", "vlr": "AND", "val": ""},
                             {"fld": "contentText", "cdr": "OR", "hlt": "true", "vlr": "AND",
                              "val": ""}]}],
                  "obs": [{"fld": "dataTime", "drt": "DESC"}]}
DataPath = os.getcwd() + r'/data'
TextPath = DataPath + r'/text_whole'
UrlPath = DataPath + '/url_whole.log'
ListPath = DataPath + '/list_whole.log'

NewsPerPage = 20


def write2csv(info_list, out_file):
    with open(out_file, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        fields = info_list[0].keys()  #
        fields = sorted(list(fields))
        # print(info_list)
        # w.writerow(fields)
        for item in info_list:
            w.writerow([item[field] for field in fields])


class Crawl:
    keyWords = []
    keyWordListSize = 0
    jsonPart = {}
    keyWordsSize = []
    searchPageList = []

    def __init__(self, key_words):
        self.keyWords = key_words
        self.keyWordListSize = len(key_words)
        self.keyWordsSize = [len(key_words[index]) for index in range(0, self.keyWordListSize)]
        self.searchPageList = []
        self.hm = HMap()
        self.urlFile = open(UrlPath, 'w+', encoding='utf-8')
        self.fileList = [''.join(item.split('-')[1:]) for item in os.listdir(TextPath)]

    def __del__(self):
        self.urlFile.close()

    def crawl_complex_search(self, startX=0, startY=0):
        if self.keyWordListSize == 2:
            print("Size of Key Word List is TWO!")
            for indexX, keyWordFirst in enumerate(self.keyWords[0]):
                indexY = 0
                if indexX < startX:
                    continue
                for indexY, keyWordSecond in enumerate(self.keyWords[1]):
                    # print(startX, startY)
                    # print(indexX, indexY)
                    if indexX <= startX and indexY < startY:
                        continue
                    self.complex_search_word = keyWordFirst + " " + keyWordSecond
                    search_page, json_part = self.crawlSearchMethod(self.complex_search_word)
                    search_result = Parser.parsingSearchMethod(search_page, json_part, self.complex_search_word)
                    self.searchPageList.append(search_result)
                    time.sleep(0.1)
                    print(str(indexX) + " " + str(indexY) + self.complex_search_word)
                    self.crawl_context_with_urls(search_result)

        elif self.keyWordListSize == 1:
            print("Size of Key Word List is ONE!")
            for indexX, keyWord in enumerate(self.keyWords[0]):
                if indexX < startX:
                    continue
                self.complex_search_word = keyWord
                search_page, json_part = self.crawlSearchMethod(self.complex_search_word)
                search_result = Parser.parsingSearchMethod(search_page, json_part, keyWord)
                self.searchPageList.append(search_result)
                time.sleep(0.1)
                print(str(indexX) + " " + self.complex_search_word)
                self.crawl_context_with_urls(search_result)

        else:
            print("Too many key words lists.")
            return

    '''获取一个搜索页面中应当爬取哪些项目'''

    def get_crawl_list(self, search_result, re_crawl=False):
        result_url_list = []
        news_url = []
        if os.access("result_url.csv", os.R_OK) and not re_crawl:
            print("result_url.csv exist")
            f = open("result_url.csv", 'r', encoding='utf-8')
            csv_reader = csv.reader(f)
            result_url_list = list(csv_reader)
            for item in result_url_list:
                news_url.append(item[1])
            return news_url

        total_page = search_result.totalCount
        # for index in range(1, int(total_page) + 1):
        for index in range(30, 90):
            list_url = BaseUrl + search_result.jsonPart + r'&pageNo=' + str(index) + '&pageSize=' + str(NewsPerPage)
            browser.get(list_url)
            time.sleep(3)
            html_doc = browser.page_source
            result = Parser.parsingSearchMethod(html_doc, search_result.jsonPart, keyWords="")
            # for index in range(0, int(search_result.totalCount) - 1):
            for i, item in enumerate(result.page.find_all('div', {'class': 'articleSum_li'})):
                title = item.find('a').text
                pub_time = item.find_all('span')[1].text[4:]
                url = 'http://data.people.com.cn' + item.find('a').get('href')
                if title not in self.fileList and "2018-01-01" <= pub_time < "2019-01-01":
                    news_url.append(url)
                    info = {'title': title, 'url': url}
                    print(info)
                    result_url_list.append(info)
                    self.fileList.append(title)
            print("Length of New Pages' Index is %d, Now In Page %d" % (len(news_url), index))
            if result_url_list:
                write2csv(result_url_list, "result_url.csv")
                result_url_list = []
        return news_url

    def crawl_context_with_urls(self, search_result):
        # totalCount = search_result.totalCount
        news_url = self.get_crawl_list(search_result)
        if news_url is None:
            print("Get New Pages' Index Fail!")
            news_url = range(0, int(search_result.totalCount) - 1)
        info_list = []
        # for index, url in enumerate(news_url):
        for index in range(0, len(news_url)):
            info = {}
            browser.get(news_url[index])
            time.sleep(3)
            html_doc = browser.page_source

            soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
            # 出现问题，循环刷新
            while soup.find('h2') is None:
                browser.get(news_url[index])
                time.sleep(3)
                html_doc = browser.page_source
                soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
                print("Re crawling news %d/%d" % (index, len(news_url)))
            info['title'] = soup.find('h2').getText().strip()
            info['href'] = news_url[index]
            info['time'] = soup.find('div', class_='fr').getText().strip()
            content_str = ""
            # 获得该页中所有的新闻项目
            p_elements = soup.find_all('p')
            for item in p_elements:
                content_str += item.getText().strip()
            info['content'] = content_str
            info_list.append(info)
            print("Now crawling news %d/%d" % (index, len(news_url)))
            if index % 30 == 0 and info_list:
                write2csv(info_list, "result.csv")
                info_list = []
        return info_list

    def crawl_url(self, search_result):
        total_page = search_result.totalCount
        for index in range(1, int(total_page) + 1):
            list_url = BaseUrl + search_result.jsonPart + r'&pageNo=' + str(index) + r'&pageSize=' + str(NewsPerPage)
            page_request = requests.get(list_url)
            # print(pageRequest)
            result = Parser.parsingSearchMethod(page_request, search_result.jsonPart, keyWords="")
            for item in result.page.div.div.div.next_sibling.next_sibling.next_sibling.next_sibling.div.next_sibling.next_sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.find_all(
                    'a', {'class': 'open_detail_link'}):
                item_url = item['href']
                hash_value = hash(item_url)
                if hash_value in self.hm.hashMap.keys():
                    continue
                self.hm.hashMap[hash_value] = 1
                self.urlFile.write(item_url + '\n')

    """获得搜索结果页"""

    def crawlSearchMethod(self, complexSearchWord):
        jsonPart = self.buildJson(complexSearchWord)
        print(BaseUrl + jsonPart)
        browser.get(
            "http://www.lib.whu.edu.cn/dc/urlto_1.asp?id=&url=http%3A%2F%2Fdata.people.com.cn&source_id=WHU06653&u=中文&title=人民数据库")
        time.sleep(3)
        browser.get(BaseUrl + jsonPart)
        time.sleep(3)
        html_doc = browser.page_source
        # try:
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #         'Chrome/51.0.2704.63 Safari/537.36'}
        #     r = requests.get(BaseUrl + jsonPart, headers=headers, timeout=30)
        #     r.raise_for_status()
        #     r.encoding = r.apparent_encoding
        #     return r, jsonPart
        #     # return requests.get(BaseUrl + jsonPart, timeout=30), jsonPart
        # except :
        #     print("exception")
        return html_doc, jsonPart

    def buildJson(self, word):
        curJsonPart = GlobalJsonPart
        for cdsElement in curJsonPart["cds"]:
            for one in cdsElement["cds"]:
                one["val"] = word
        return json.dumps(curJsonPart)


class HMap:
    def __init__(self):
        self.hashMap = {}
