# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from News.items import NewsItem
class NewsPipeline(object):
    def open_spider(self,spider):
        self.conn=MongoClient(host="127.0.0.1",port=27017)
        self.client=self.conn.news.wenshu
    def process_item(self, item, spider):
        if isinstance(item,NewsItem):
            self.client.update(dict(item))
        return item

