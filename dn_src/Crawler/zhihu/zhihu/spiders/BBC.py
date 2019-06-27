import json

from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy import Request
import datetime
import re
import csv

class BBCSpider():
    name = 'bbc'
    keyword='食品安全'
    filename="./bbc.csv"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17'
    }
    def start_requests(self):
        req_url = "http://www.bbc.co.uk/search?q=" + self.keyword + "&sa_f=search-product&filter=news&suggid="
        page = 1
        yield Request(req_url, self.parse, meta={'keyword': self.keyword, 'page': page},headers=self.headers)

    def filter_tags(self, htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        pattern = re.compile(r'"')
        contents = pattern.sub("'", s)
        return contents

    def parse(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']
        selector = Selector(response)
        contents = selector.xpath('//section[@class="search-content"]/ol/li')
        pub_time = datetime.datetime.today()
        for content in contents:
            item = {}
            item['keyword'] = keyword.encode('utf-8')
            url = content.xpath('./article/a[@class="rs_touch"]/@href').extract()[0]
            item["url"] = url.encode('utf-8')
            date_time = content.xpath('./article/aside/dl/dd/time/@datetime').extract()[0]
            num_pattern = re.compile(r'\d+')
            numArr = num_pattern.findall(date_time)
            pub_time = datetime.datetime(int(numArr[0]), int(numArr[1]), int(numArr[2]))
            item["pubdate"] = pub_time
            yield Request(url, callback=self.parse_news, meta={'item': item})

        page = int(page) + 1
        nexturl = "http://www.bbc.co.uk/search?q=" + keyword + "&sa_f=search-product&filter=news&suggid=#&page=" + str(
            page)
        yield Request(nexturl, self.parse, meta={'keyword': keyword, 'page': page})

    def parse_news(self, response):
        item = response.meta['item']
        selector = Selector(response)
        item["publisher"] = "BBC"
        item["title"] = selector.xpath('//div[@class="story-body"]/h1/text()').extract()[0].encode('utf-8')
        item["source"] = "BBC"

        # 分成了好多小段落，需要拼接起来
        paras = selector.xpath('//div[@class="story-body__inner"]/p').extract()
        content = "\n".join(paras)

        item["content"] = self.filter_tags(content).encode('utf-8')
        if len(paras) > 0:
            self.save(self.filename,item)

    def save(self,filename, item):
        with open(filename, 'a+', encoding='utf-8', newline='') as f:
            # f = open(filename,'a+',encoding='utf-8',newline = '')
            writer = csv.writer(f, dialect="excel")
            writer.writerow([item['keyword'], item['url'], item['pubdate'],item["title"],item["content"]])