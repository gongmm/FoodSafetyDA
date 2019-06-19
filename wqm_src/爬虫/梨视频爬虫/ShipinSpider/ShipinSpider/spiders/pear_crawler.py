import json
from scrapy import Request
from scrapy import Selector
from datetime import datetime
import re
from scrapy.spiders import CrawlSpider
from ShipinSpider.items import ShipinspiderItem
import time

import scrapy
import csv
from bs4 import BeautifulSoup
from scrapy.http import Request
from selenium import webdriver



#爬取梨视频数据
class PearVideoSpider(CrawlSpider):
    name = 'pearvideo_crawler'
    root_url = 'http://www.pearvideo.com/'
    st_url = 'http://www.pearvideo.com/search.jsp?start='
    headers = {"Referer":"https://www.pearvideo.com/sear…p?start=0&k=%E9%A3%9F%E5%93%81"} #自定义请求头 解决动态加载问题
    keyword = '食品'  #定义爬取关键词
    starttime = '2017-01-01'    #设置爬虫开始时间
    endtime = '2017-12-31'  #设置爬虫结束时间范围


    #重写start_requests
    def start_requests(self):
        for num in range(0,1400,10):    #搜索出1400条结果
            print('***********开始爬取首页')
            print(num)
            start_url = self.st_url+str(num)+'&k='+self.keyword
            print(start_url)
            yield Request(url=start_url,headers=self.headers,callback=self.parse)

    #判断时间是否在搜索范围内
    def is_date_valid(self,search_date):
        start_time = datetime.strptime(self.starttime, "%Y-%m-%d")
        end_time = datetime.strptime(self.endtime, "%Y-%m-%d")
        return (search_date >= start_time and search_date <= end_time)

    #解析初始页面
    def parse(self, response):
        selector = Selector(response)
        results = selector.xpath('//*[@id="mainPage"]/li[@class="result-list"]')
        for r in results:
            date_text = r.xpath('.//div[@class="publish-time"]/text()').extract()[0][3:]
            date_text = date_text.split('-')
            search_date = datetime(int(date_text[0]), int(date_text[1]), int(date_text[2]))
            #if True:
            if self.is_date_valid(search_date):
                # 发布时间符合条件的，继续爬取视频的详细信息
                video_url = self.root_url + r.xpath('.//div[@class="list-right"]/a/@href').extract()[0]
                yield Request(video_url, headers=self.headers,meta={ 'pubdate': search_date}, callback=self.parse_content)

    #解析单个视频页面
    def parse_content(self, response):
        selector = Selector(response)
        item = ShipinspiderItem()
        item['keyword'] = self.keyword
        item['pubdate'] = str(response.meta['pubdate'])
        item['title'] = selector.xpath('//h1[@class="video-tt"]/text()').extract()[0]
        script = selector.xpath('//script[@type="text/javascript"]').extract()
        for s in script:
            pattern = re.compile(r'srcUrl="(http.*?)"', re.I | re.M)
            url = pattern.findall(s)
            if url:
                video_source = url[0]
                item['source'] = video_source
                break
        yield item
