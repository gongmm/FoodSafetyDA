from urllib.parse import urlencode
from scrapy import Request
import scrapy
import json
from pyquery import PyQuery
import csv
from mWeiboSpider.items import WeiBoSpiderItem


class WeiBoSpider(scrapy.Spider):
    name = 'weibo'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "MWeibo-Pwa": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    page = 1

    def get_url(self, keyword):
        start_url = 'https://m.weibo.cn/api/container/getIndex?'
        params = {
            'containerid': '100103type=1&q=' + keyword,
            'page_type': 'searchall',
            'page': self.page
        }
        start_url = start_url + urlencode(params)
        print(start_url)
        return start_url

    def start_requests(self):
        # with open('food_topic.csv', 'r',
        #           encoding='utf-8-sig') as csv_file:
        #     reader = csv.DictReader(csv_file)
        #     for row in reader:
        #         keyword=''
        #         print (row)
        #         topic = row['topic'].split()[:3]
        #         topic_id=row['topic_id']
        #         for i in range(len(topic)):
        #             keyword = keyword + '' + topic[i]
        #         yield Request(url=self.get_url(keyword), callback=self.parse,headers=self.headers,
        #                       meta={'keyword':keyword,'topic_id':topic_id})

        # keyword = '海鲜 小龙虾 武汉'
        keyword = '疫情 禽流感'
        topic_id = 21
        yield Request(url=self.get_url(keyword), callback=self.parse, headers=self.headers,
                      meta={'keyword': keyword, 'topic_id': topic_id})

    def parse(self, response):
        has_next = True
        keyword = response.meta['keyword']
        topic_id = response.meta['topic_id']
        json_text = json.loads(response.text)
        if json_text.get('ok') == 1:
            if json_text['data']['cards']:
                for cards in json_text['data']['cards']:
                    if cards.get('card_group'):
                        for card in cards['card_group']:
                            # 获得搜索的微博信息
                            if card.get('mblog'):
                                item = WeiBoSpiderItem()
                                # 获得微博发布时间
                                item['time'] = card['mblog']['created_at']
                                # 获得微博内容
                                if card.get('mblog').get('longText'):
                                    content = card['mblog']['longText']['longTextContent']
                                    item['content'] = content.strip()
                                elif card.get('mblog').get('text'):
                                    content = PyQuery(card['mblog']['text']).text()
                                    item['content'] = content.strip()
                                # 获得话题 id
                                item['topic_id'] = topic_id
                                # 获得关键词
                                item['topic'] = keyword
                                # 获得转发数
                                item['reposts_count'] = card['mblog']['reposts_count']
                                # 获得评论数
                                item['comments_count'] = card['mblog']['comments_count']
                                # 获得点赞数
                                item['attitudes_count'] = card['mblog']['attitudes_count']
                                yield item
                    else:
                        if cards.get('mblog'):
                            item = WeiBoSpiderItem()
                            item['time'] = cards['mblog']['created_at']
                            if cards.get('mblog').get('longText'):
                                item['content'] = cards['mblog']['longText']['longTextContent']
                                print(item['content'])
                            elif cards.get('mblog').get('text'):
                                item['content'] = PyQuery(cards['mblog']['text']).text()
                            item['topic_id'] = topic_id
                            item['topic'] = keyword
                            # 获得转发数
                            item['reposts_count'] = cards['mblog']['reposts_count']
                            # 获得评论数
                            item['comments_count'] = cards['mblog']['comments_count']
                            # 获得点赞数
                            item['attitudes_count'] = cards['mblog']['attitudes_count']
                            yield item
        else:
            # 停止爬取下一页
            has_next = False
        if has_next:
            self.page += 1
            yield Request(self.get_url(keyword), callback=self.parse, headers=self.headers,
                          meta={'keyword': keyword, 'topic_id': topic_id})
        else:
            self.page = 1
