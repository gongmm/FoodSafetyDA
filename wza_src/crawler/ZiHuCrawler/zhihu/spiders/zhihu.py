# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from scrapy import Request
import scrapy
import json
from pyquery import PyQuery
import csv
from zhihu.items import ZhiHuItem
import re
import time


class ZhiHuSpider(scrapy.Spider):
    name = 'zhihu'
    headers = {

        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    page = 1
    keyword = '食品'

    def get_url(self, keyword):
        start_url = 'https://www.zhihu.com/api/v4/search_v3?'
        params = {
            't': 'general',
            'q': keyword,
            'correction': 1,
            'offset': 20,
            'limit': 20,
            'lc_idx': 26
        }
        start_url = start_url + urlencode(params)
        print(start_url)
        return start_url

    def start_requests(self):

        keyword = '食品'
        yield Request(url=self.get_url(keyword), callback=self.parse, headers=self.headers, meta={'keyword': keyword})

    def parse(self, response):
        has_next = True
        keyword = response.meta['keyword']
        # json_text=response.text
        # print(response.text)
        json_text = json.loads(response.text)
        if json_text['paging']['is_end'] == False:
            for data in json_text['data']:
                item = ZhiHuItem()
                if data.get('object'):
                    if data.get('object').get('content'):
                        content = data['object']['content']
                        content_without_tag = re.sub(r'<.*?>', '', content)
                        content_without_tag = content_without_tag.replace('\n', '')
                        item['content'] = content_without_tag

                        date_array = time.localtime(data['object']['created_time'])
                        date = time.strftime("%Y-%m-%d %H:%M:%S", date_array)
                        item['pub_date'] = date
                    if data.get('object').get('question'):
                        if data.get('object').get('question').get('name'):
                            content = data['object']['question']['name']
                            content_without_tag = re.sub(r'<.*?>', '', content)
                            item['question'] = content_without_tag
                            item['keyword'] = keyword
                            if "2018-01-01 00:00" < item['pub_date'] < "2019-01-01 00:00":
                                yield item
                            else:
                                pass

        else:
            # 停止爬取下一页
            has_next = False
        if has_next:
            # self.page+=1
            url = json_text['paging']['next']
            yield Request(url=url, callback=self.parse, headers=self.headers, meta={'keyword': keyword})
