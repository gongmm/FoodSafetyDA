import scrapy
import csv
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider
from crawler.items import CrawlerItem
from scrapy.http import Request


class Crawler_1(CrawlSpider):
    name = 'crawler_1'  #scrapy crawler ***指定名字

    #读取csv文件，将url保存为list
    def read_csv(self):
        filename = '/Users/Amanda/Desktop/大四/毕设/爬虫/url分类爬虫/urls/newspeople_1.csv' #需要读取对的文件路径
        with open(filename, encoding="unicode_escape") as f:
            f_csv = csv.reader(f)
            url_list = []
            for row in f_csv:
                url_list.append(row) #提取url
        return url_list

    #重写start_requests
    def start_requests(self):
        url_list = self.read_csv()
        for url_l in url_list:
            url = ''.join(url_l)    #request里的url要求为str
            yield Request(url=url,callback=self.parse)


    def parse(self, response):
        item = CrawlerItem() #将数据存入item
        html = response.body
        bf = BeautifulSoup(html, 'html.parser',from_encoding='gb18030') #beautifulsoup解析网页
        url = response.url  #url
        keyword = bf.find('meta', attrs={'name': 'keywords'}).get('content')  # keyword
        pudate = bf.find('meta', attrs={'name': 'publishdate'}).get('content')  # pudate 发布时间
        title = bf.find('title').getText()  # title
        div_bf = bf.find('div', attrs={'class': 'box_con'})  # content
        p = div_bf.find_all('p')
        content =''
        for each in p:
            content= content+str((each.getText()))
        imglist = []
        if div_bf.find_all('img'):
            img = div_bf.find_all('img')
            for each in img:
                imglist.append(each.get('src'))
        else:
            imglist =[]

        item['url'] = url
        item['keyword'] = keyword
        item['pudate'] = pudate
        item['title'] = title
        item['content'] = content
        item['imglist'] =imglist
        yield item



