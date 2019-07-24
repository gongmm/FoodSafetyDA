# coding=utf-8
import scrapy
from scrapy.selector import Selector
from News.items import NewsItem
import re
from scrapy import Request
import json


class QQNews(scrapy.Spider):
    name = 'qqnews'
    keyword = '瘦肉精'
    page = 1
    # start_url='https://www.sogou.com/sogou?site=news.qq.com&query='+keyword+'&page='+str(page)
    # start_urls=[
    #     start_url
    # ]
    url_prefix = "https://www.sogou.com/sogou"
    hasNext = True

    def start_requests(self):
        keyword = self.keyword
        start_url = 'https://www.sogou.com/sogou?site=news.qq.com&query=' + keyword + '&page=1'
        yield Request(start_url, self.parse, meta={'keyword': keyword})

    def parse(self, response):
        sel = Selector(response)
        pic_content = sel.xpath("//div[@id='main']/div[3]//div[@class='vrwrap']")
        word_content = sel.xpath("//div[@id='main']/div[3]//div[@class='rb']")
        for vrwrap in pic_content:
            url = vrwrap.xpath("./h3[@class='vrTitle']/a/@href").extract()[0]
            title = vrwrap.xpath("./h3[@class='vrTitle']/a/text()").extract_first()
            source = vrwrap.xpath(
                "./div[@class='strBox']/div[@class='str_info_div']/div[@class='fb']/cite/text()").extract_first()
            source_url = ""
            if not source is None:
                source_url = source.split('-')[0].strip()
            if not url is None:
                yield scrapy.Request(url="https://www.sogou.com" + url, callback=self.parsedetail,
                                     meta={'source': source_url})
        for fb in word_content:
            url = fb.xpath("./h3[@class='pt']/a/@href").extract_first()
            title = fb.xpath("./h3[@class='pt']/a/text()").extract_first()
            source = fb.xpath("./div[@class='fb']/cite/text()").extract_first()
            source_url = ""
            if not source is None:
                source_url = source.split('-')[0].strip()
                # sources.append(source)
            if not url is None:
                yield scrapy.Request(url="https://www.sogou.com" + url, callback=self.parsedetail,
                                     meta={'source': source_url})
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

    def parsedetail(self, response):
        source_url = response.meta["source"]
        html_script = r'<script>(.*?)</script>'
        m_script = re.findall(html_script, response.body.decode('utf-8'), re.S | re.M)
        url_script = r'"(.*?)"'
        url = re.findall(url_script, m_script[0], re.S | re.M)
        time = url[0].split('/')[-2]
        id = url[0].split('/')[-1].split('.')[0]
        newsid = time + id + '00'
        request_url = "https://openapi.inews.qq.com/getQQNewsNormalContent?id=" + newsid + "&chlid=news_rss&refer=mobilewwwqqcom&otype=jsonp&ext_data=all&srcfrom=newsapp&callback=getNewsContentOnlyOutput"
        # last_url="https://new.qq.com/cmsn/"+time+"/"+newsid
        yield scrapy.Request(url=request_url, callback=self.parsecontent,
                             meta={'pubdate': time})

    def parsecontent(self, response):
        pubdate = response.meta["pubdate"]
        g = re.search("getNewsContentOnlyOutput\\((.+)\\)", response.body.decode('utf-8'))
        data_json = json.loads(g.group(1))
        ret = data_json["ret"]
        if ret == 0:
            try:
                item = NewsItem()
                item['title'] = data_json["title"]
                item['pubdate'] = pubdate
                item['content'] = data_json["content"][-1]
                item['url'] = data_json["url"]
                item['keyword'] = self.keyword
                yield item
            except Exception as e:
                print(e.message)
        else:
            pass
