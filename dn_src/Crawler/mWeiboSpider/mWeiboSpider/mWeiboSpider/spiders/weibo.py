from urllib.parse import urlencode
from scrapy import Request
import scrapy
import json
from pyquery import PyQuery
import csv
from mWeiboSpider.items import weibospiderItem
class weioSpider(scrapy.Spider):
    name='weibo'
    headers={
        "Accept": "application/json, text/plain, */*",
        "MWeibo-Pwa": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    page=1


    def get_url(self,keyword):
        start_url='https://m.weibo.cn/api/container/getIndex?'
        params = {
            'containerid': '100103type=1&q='+keyword,
            'page_type': 'searchall',
            'page': self.page
        }
        start_url=start_url + urlencode(params)
        print(start_url)
        return start_url
    def start_requests(self):
        # with open('E:\\pySpace\\MachineLearning\\ldatest\\csv\\testcsv\shipintopic.csv', 'r',
        #           encoding='utf-8-sig') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         keyword=''
        #         print (row)
        #         topic = row['topic'].split()[:3]
        #         topicid=row['topicid']
        #         for i in range(len(topic)):
        #             keyword = keyword + '' + topic[i]
        #         yield Request(url=self.get_url(keyword), callback=self.parse,headers=self.headers,meta={'keyword':keyword,'topicid':topicid})
        keyword='食盐 批发 盐业'
        topicid=3
        yield Request(url=self.get_url(keyword), callback=self.parse,headers=self.headers,meta={'keyword':keyword,'topicid':topicid})
    def parse(self,response):
        hasNext=True
        keyword=response.meta['keyword']
        topicid=response.meta['topicid']
        json_text=json.loads(response.text)
        if json_text.get('ok')==1:
            if json_text['data']['cards']:
                for item in json_text['data']['cards']:
                    for card in item['card_group']:
                        if card.get('mblog'):
                            item=weibospiderItem()
                            item['time']=card['mblog']['created_at']
                            if card.get('mblog').get('longText'):
                                item['content']=card['mblog']['longText']['longTextContent']
                                #print(card['mblog']['longText']['longTextContent'])
                            elif card.get('mblog').get('text'):
                                item['content']=PyQuery(card['mblog']['text']).text()
                                #print(PyQuery(card['mblog']['text']).text())
                            item['topicid']=topicid
                            item['topic']=keyword
                            yield item
        else:
            #停止爬取下一页
           hasNext=False
        if hasNext:
            self.page+=1
            yield Request(self.get_url(keyword),callback=self.parse,headers=self.headers,meta={'keyword':keyword,'topicid':topicid})
        else:
            self.page=1
