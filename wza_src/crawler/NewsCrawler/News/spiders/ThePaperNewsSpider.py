# coding=utf-8
import scrapy
from scrapy.selector import Selector
from News.items import NewsItem
import re
from scrapy import Request
import json


class PengPaiNews(scrapy.Spider):
    name = 'thepaper'
    keyword = '非洲猪瘟'
    page = 0  # 起始页数
    headers = {
        'Cookie': 'UM_distinctid=167a7e917df2c-0b6c288b7de30f-3a3a5e0e-100200-167a7e917e0a3; paperSearhType=1; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=E3C35146EE53F46D9A79BEAC70BCC6EC; uuid=7b14f799-9c64-44a5-82af-97b4be91a951; SERVERID=srv-omp-ali-portal10_80; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1544710334,1544946497,1544950370; CNZZDATA1261102524=1617399195-1544709571-null%7C1544948284; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1544951896; UM_distinctid=167a7e917df2c-0b6c288b7de30f-3a3a5e0e-100200-167a7e917e0a3; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1544710334,1544946497,1544950370; __ads_session=sa3BZ9FoNQkhy4UCLQA=; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1544951896; __ads_session=yei5R1lrNQklDcYCLQA=',
        'Referer': 'https://www.thepaper.cn/searchResult.jsp?inpsearch=%E5%9C%B0%E6%B2%9F%E6%B2%B9'
    }
    url_prefix = 'https://www.thepaper.cn/'

    def start_requests(self):
        keyword = self.keyword
        start_url = 'https://www.thepaper.cn/load_search.jsp?k=' + keyword + '&pagesize=10&searchPre=all_0:&orderType=1&pageidx=' + str(
            self.page)
        print("start_url: " + start_url)
        yield Request(start_url, self.parse, meta={'keyword': keyword}, headers=self.headers)

    def parse(self, response):
        if response.body != '':
            sel = Selector(response)
            searches = sel.xpath('//div[@class="search_res"]')
            for search in searches:
                link = search.xpath('./h2/a/@href').extract_first()
                title_list = search.xpath('./h2/a/text()').extract()
                title = ""
                for item in title_list:
                    title += item
                pubdate = search.xpath(
                    './div[@class="search_trbs"]/a/preceding-sibling::span[1]/text()').extract_first()
                if "2018-01-01" <= pubdate < "2019-01-01":
                    print("Valid: " + pubdate)
                    yield Request(url=self.url_prefix + link, callback=self.parsedetail,
                                  meta={"source": self.url_prefix + link, "title": title, "pubdate": pubdate})
                else:
                    print("Invalid: " + pubdate)
                    pass

            self.page = self.page + 1
            next_page = 'https://www.thepaper.cn/load_search.jsp?k=' + self.keyword + '&pagesize=10&searchPre=all_0:&orderType=1&pageidx=' + str(
                self.page)
            print("next_url: " + next_page)
            yield Request(next_page, self.parse, headers=self.headers)

    def parsedetail(self, response):
        sel = Selector(response)
        title = response.meta['title']
        source = response.meta['source']
        contentlist = sel.xpath('//div[@class="news_txt"]//text()').extract()
        pubdate = response.meta['pubdate']
        print(pubdate)
        contentstr = ""
        for content in contentlist:
            contentstr = contentstr + content

        item = NewsItem()
        item['keyword'] = self.keyword
        item['title'] = title
        item['pubdate'] = pubdate
        item['url'] = source
        item['content'] = contentstr
        yield item
