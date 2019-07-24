# coding=utf-8
import scrapy
from scrapy.selector import Selector
from News.items import NewsItem
import re
from scrapy import Request
import json
from bs4 import BeautifulSoup


class QQNews(scrapy.Spider):
    name = 'sougou'
    keyword = '食品安全'
    page = 1
    # start_url='https://www.sogou.com/sogou?site=news.qq.com&query='+keyword+'&page='+str(page)
    # start_urls=[
    #     start_url
    # ]
    url_prefix = "https://news.sogou.com/news"
    # "https://news.sogou.com/news?query=%CA%B3%C6%B7%B0%B2%C8%AB&page=20&p=17040300&dp=1"
    hasNext = True

    def start_requests(self):
        keyword = self.keyword
        start_url = 'https://news.sogou.com/news?query=' + keyword + '&page=1&p=17040300&dp=1'
        yield Request(start_url, self.parse, meta={'keyword': keyword})

    def parse(self, response):
        sel = Selector(response)
        # soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
        title_source_list = sel.xpath("//div[@class='vrwrap']//h3[@class='vrTitle']")
        title_result_list = []
        for content in title_source_list:
            title_str = ""
            for component in content.xpath(".//text()").extract():
                title_str += component.strip()
            title_result_list.append(title_str)

        time_source_list = sel.xpath("//p[@class='news-from']/text()").extract()
        time_result_list = []
        for content in time_source_list:
            time_result_list.append(content.split()[-1])

        href_result_list = sel.xpath("//div[@class='vrwrap']//h3[@class='vrTitle']/a/@href").extract()

        # 爬取具体内容
        # for url in href_result_list:
        #     yield scrapy.Request(url=url, callback=self.parse_content,
        #                          meta={'source': url})
        for index in range(len(title_result_list)):

            item = NewsItem()
            item['title'] = title_result_list[index]
            item['pubdate'] = time_result_list[index]
            item['content'] = ""
            item['url'] = href_result_list[index]
            item['keyword'] = self.keyword
            yield item

        # find out if there is the next page 是否还有下一页
        if sel.xpath('//a[@id="sogou_next"]').extract():
            self.hasNext = True
        else:
            self.hasNext = False
        if self.hasNext:
            # 下一页的链接（相对位置）
            next_relative__url = sel.xpath('//a[@id="sogou_next"]/@href').extract()[0]
            next_url = self.url_prefix + next_relative__url
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse, cookies=[])

    # def parse_content(self, response):
    #     pubdate = response.meta["pubdate"]
    #     g = re.search("getNewsContentOnlyOutput\\((.+)\\)", response.body.decode('utf-8'))
    #     data_json = json.loads(g.group(1))
    #     ret = data_json["ret"]
    #     if ret == 0:
    #         try:
    #             item = NewsItem()
    #             item['title'] = data_json["title"]
    #             item['pubdate'] = pubdate
    #             item['content'] = data_json["content"][-1]
    #             item['url'] = data_json["url"]
    #             item['keyword'] = self.keyword
    #             yield item
    #         except Exception as e:
    #             print(str(e))
    #     else:
    #         pass
